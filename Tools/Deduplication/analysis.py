#coding=utf-8

import subprocess as subpro
import os
import hashlib
import json
import sys
import datetime

from sqlalchemy.sql import column
import pandas as pd
import numpy as np

import database as db
from dockerhub import Dockerhub

class Load:

    __DOCKER_PATH = '/var/lib/docker/'
    __OVERLAY2_PATH = __DOCKER_PATH + 'overlay2/'
    __DIFFID2DIGEST_PATH = __DOCKER_PATH + 'image/overlay2/distribution/v2metadata-by-diffid/sha256/'
    __DIGEST2DIFFID_PATH = __DOCKER_PATH + 'image/overlay2/distribution/diffid-by-digest/sha256/'
    __LAYERDB_PATH = __DOCKER_PATH + 'image/overlay2/layerdb/sha256/'

    def __init__(self, Session) -> None:
        self.__Session = Session
        self.__repository_num = 0
        self.__image_stat = {'num': 0, 'total_size': 0, 'max_size': 0, 'min_size': sys.maxsize}
        self.__layer_stat = {'num': 0, 'total_size': 0, 'max_size': 0, 'min_size': sys.maxsize}
        self.__file_stat = {'num': 0, 'total_size': 0, 'max_size': 0, 'min_size': sys.maxsize}

    def __execute_shell_command(self, command):
        out = subpro.Popen(command, shell=True, stdout=subpro.PIPE, stderr=subpro.PIPE)
        std_out, std_err = out.communicate()
        return_code = out.returncode
        assert return_code == 0, '[command] %s, [error] %s' %(command, str(std_err, encoding='utf-8'))
        return str(std_out, encoding='utf-8')

    def __statistic(self, item: dict, stat: dict):
        stat['num'] += 1
        sz = item.get('size', 0)
        stat['total_size'] += sz
        stat['min_size'] = min(stat['min_size'], sz)
        stat['max_size'] = max(stat['max_size'], sz)

    def __repositories(self):
        out = self.__execute_shell_command('docker images')
        repos = {}
        for info in out.split('\n')[1:-1]:
            info = info.split()
            repo, tag = info[0], info[1]
            if repo not in Dockerhub.get_repos_all():
                continue
            if repo not in repos:
                repos[repo] = []
            repos[repo].append(tag)
        self.__repository_num = len(repos)
        return repos
    
    def __images(self, repository, tag):
        image = repository + ':' + tag
        command = 'docker image inspect ' + image
        out = self.__execute_shell_command(command)
        image_info = json.loads(out)
        assert len(image_info) == 1,\
            '[command] %s, [output] length %d not equal 1' %(command, len(image_info))
        image_info = image_info[0]
        res = {
            'tag': tag,
            'digest': image_info['Id'],
            'repo_digest': image_info['RepoDigests'][0][len(repository + '@'):],
            'size': int(image_info['Size']),
            'layer_num': len(image_info['RootFS']['Layers'])
        }
        self.__statistic(res, self.__image_stat)
        return res
    
    def __layers(self, repository, tag) -> list:
        image = repository + ':' + tag
        out = self.__execute_shell_command('docker image inspect ' + image)
        image_info = json.loads(out)
        assert len(image_info) == 1,\
            'found %d manifest [image] %s' %(len(image_info), image)
        image_info = image_info[0]
        
        diff_ids = image_info['RootFS']['Layers']

        tmp_str = image_info['GraphDriver']['Data'].get('LowerDir', '')
        abs_paths = tmp_str.split(':')[::-1] if len(tmp_str) > 0 else []
        abs_paths.append(image_info['GraphDriver']['Data']['UpperDir'])

        cache_ids = [path[len(self.__OVERLAY2_PATH): -len('/diff')] for path in abs_paths]

        tmp_digests = []
        for i, diff_id in enumerate(diff_ids):
            command = 'cat %s%s' %(self.__DIFFID2DIGEST_PATH, diff_id[len('sha256:'): ])
            infos = json.loads(self.__execute_shell_command(command))
            digest = [info['Digest'] for info in infos if info['SourceRepository'] == repository]
            for dgst in digest:
                    cmd = 'cat %s%s' %(self.__DIGEST2DIFFID_PATH, dgst[len('sha256:'): ])
                    if self.__execute_shell_command(cmd) == diff_id:
                        tmp_digests.append(dgst)
                        break
            if len(tmp_digests) != i + 1:
                tmp_digests.append('NULL')
            assert len(tmp_digests) == i + 1,\
                'miss one digest [diff id] %s, [repository] %s' %(diff_id, repository)

        chain_ids = []
        chain_id = diff_ids[0][len('sha256:'):]
        for i in range(len(diff_ids)):
            if i != 0:
                s = chain_ids[-1]['chain_id'] + ' ' + diff_ids[i]
                chain_id = hashlib.sha256(s.encode()).hexdigest()
            path = os.path.join(self.__LAYERDB_PATH, chain_id)
            cache_id = self.__execute_shell_command('cat %s/cache-id' %path)
            assert cache_id == cache_ids[i],\
                'cache_id mismatched [inspect] %s, [found] %s' %(cache_ids[i], cache_id)
            diff_id = self.__execute_shell_command('cat %s/diff' %path)
            assert diff_id == diff_ids[i],\
                'diff_id mismatched [inspect] %s, [found] %s' %(diff_ids[i], diff_id)
            uncompressed_size = int(self.__execute_shell_command('cat %s/size' %path))
            chain_ids.append({
                'chain_id': 'sha256:' + chain_id,
                'uncompressed_size': uncompressed_size
            })
        
        res = []
        for i in range(len(diff_ids)):
            record = {
                'digest': tmp_digests[i],
                'diff_id': diff_ids[i],
                'chain_id':chain_ids[i]['chain_id'],
                'cache_id': cache_ids[i],
                'abs_path': abs_paths[i],
                'compressed_size': 0,
                'uncompressed_size': chain_ids[i]['uncompressed_size'],
                'size': chain_ids[i]['uncompressed_size']
            }
            self.__statistic(record, self.__layer_stat)
            res.append(record)
        return res

    def __files(self, layer_path, image_size, chunk_size = 1 << 20):
        res = []
        for abs_parent, _, file_names in os.walk(layer_path):
            for file_name in file_names:
                abs_path = os.path.join(abs_parent, file_name)
                if not os.path.isfile(abs_path):
                    continue
                size = os.path.getsize(abs_path)
                if size > image_size:
                    continue
                md5 = hashlib.md5()
                with open(abs_path, 'rb') as f:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    md5.update(chunk)
                record = {
                    'name': file_name.encode('utf-8').decode('utf-8'),
                    'abs_path': abs_path.encode('utf-8').decode('utf-8'),
                    'root_path': abs_path[len(self.__DOCKER_PATH):].encode('utf-8').decode('utf-8'),
                    'md5': 'md5:' + md5.hexdigest(),
                    'size': size
                }
                self.__statistic(record, self.__file_stat)
                res.append(record)
        return res

    def into_database(self):
        cur, total, delta, bound = 0, 0, 0.05, 0
        candidate_repos, candidate_images = Dockerhub.get_repos_all(), Dockerhub.get_images_all()
        with self.__Session.begin() as session:

            def flush_into_database(item):
                session.add(item)
                session.flush()
                return item.id

            repositories = self.__repositories()
            total = len(repositories)
            for repository, tags in repositories.items():
                if repository not in candidate_repos:
                    continue
                repo_id = flush_into_database(db.Repository(name=repository))
                for tag in tags:
                    repo_tag = repository + ':' + tag
                    if repo_tag not in candidate_images:
                        continue
                    image = self.__images(repository, tag)
                    image_id = flush_into_database(db.Image(
                        tag=image['tag'],
                        digest=image['digest'],
                        repo_digest=image['repo_digest'],
                        size=image['size'],
                        layer_num=image['layer_num'],
                        repo_id=repo_id
                    ))
                    for level, layer in enumerate(self.__layers(repository, tag)):
                        layer_id = flush_into_database(db.Layer(
                            digest=layer['digest'],
                            diff_id=layer['diff_id'],
                            chain_id=layer['chain_id'],
                            cache_id=layer['cache_id'],
                            level=level,
                            abs_path=layer['abs_path'],
                            compressed_size=layer['compressed_size'],
                            uncompressed_size=layer['uncompressed_size'],
                            repo_id=repo_id,
                            image_id=image_id
                        ))
                        for file in self.__files(layer['abs_path'], image['size']):
                            flush_into_database(db.File(
                                name=file['name'],
                                abs_path=file['abs_path'],
                                root_path=file['root_path'],
                                md5=file['md5'],
                                size=file['size'],
                                repo_id=repo_id,
                                image_id=image_id,
                                layer_id=layer_id
                            ))
                
                cur += 1
                if cur / total > bound:
                    print('complete %d / %d, %s' %(cur, total, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    bound += delta
        print('[Repository] num: %d' %self.__repository_num)
        print('[Image] num: %d, total size: %d bytes, minimum size: %d bytes, maximum size: %d bytes'\
            %(self.__image_stat['num'], self.__image_stat['total_size'], self.__image_stat['min_size'], self.__image_stat['max_size']))
        print('[Layer] num: %d, total size: %d bytes, minimum size: %d bytes, maximum size: %d bytes'\
            %(self.__layer_stat['num'], self.__layer_stat['total_size'], self.__layer_stat['min_size'], self.__layer_stat['max_size']))
        print('[File] num: %d, total size: %d bytes, minimum size: %d bytes, maximum size: %d bytes'\
            %(self.__file_stat['num'], self.__file_stat['total_size'], self.__file_stat['min_size'], self.__file_stat['max_size']))


class Query:

    NUM_LINES_PER_EPOCH = 1000

    def __init__(self, Session) -> None:
        self.__Session = Session

    def __group_by_field0_field1(self, Table, field0: str, value, field1: str):
        res = {}
        with self.__Session.begin() as session:
            for model in session.query(Table).filter(column(field0) == value).\
                yield_per(self.NUM_LINES_PER_EPOCH):
                item = model.to_dict()
                if item[field1] not in res:
                    res[item[field1]] = []
                res[item[field1]].append(item)
        return res

    def images2files_group_by_field(self, field: str):
        res = {}
        with self.__Session.begin() as session:
            for repo in session.query(db.Repository).yield_per(self.NUM_LINES_PER_EPOCH):
                for tag in session.query(db.Image).filter(db.Image.repo_id == repo.id).\
                    yield_per(self.NUM_LINES_PER_EPOCH):
                    res[repo.name + ':' + tag.tag] = self.__group_by_field0_field1(db.File, 'image_id', tag.id, field)
        return res


class Redundancy:

    def __init__(self, Session) -> None:
        self.__querier = Query(Session)

    def redundancy_file_level(self, data_path: str):
        repo2flag = Dockerhub.repo2scenario()
        new_images, old_images = Dockerhub.get_images_with_new_version(), Dockerhub.get_images_with_old_version()
        all_images = self.__querier.images2files_group_by_field('md5')
        new2olds = {}
        for new_image in new_images:
            if new_image not in all_images:
                continue
            repo = new_image.split(':')[0]
            for old_image in old_images:
                if old_image.split(':')[0] == repo and old_image in all_images:
                    if new_image not in new2olds:
                        new2olds[new_image] = []
                    new2olds[new_image].append(old_image)
        registry = {}
        for _, old_images in new2olds.items():
            for old_image in old_images:
                if old_image in all_images:
                    registry[old_image] = all_images[old_image]
                    break
        redundancy_list_old, redundancy_list_registry_with = {}, {}
        for scenario in Dockerhub.scenarios():
            redundancy_list_old[scenario] = []
            redundancy_list_registry_with[scenario] = []
        for new_image in new_images:
            if new_image not in new2olds:
                continue
            old_versions = new2olds[new_image]
            new_files = all_images[new_image]
            # old version
            total_size = 0
            redundancy_old = 0
            for md5, files in new_files.items():
                size = files[0]['size']
                for old_version in old_versions:
                    if md5 in all_images[old_version]:
                        redundancy_old += len(files) * size
                        break
                total_size += len(files) * size
            #registry with its repo
            redundancy_registry_with = 0
            for md5, files in new_files.items():
                size = files[0]['size']
                for _, files_registry in registry.items():
                    if md5 in files_registry:
                        redundancy_registry_with += len(files) * size
                        break
            redundant_percent_old = redundancy_old / total_size
            redundant_percent_registry_with = redundancy_registry_with / total_size        
            flag = repo2flag[new_image.split(':')[0]]
            if flag & Dockerhub.AI != 0:
                redundancy_list_old['ai'].append(redundant_percent_old)
                redundancy_list_registry_with['ai'].append(redundant_percent_registry_with)
            if flag & Dockerhub.EDGE != 0:
                redundancy_list_old['edge'].append(redundant_percent_old)
                redundancy_list_registry_with['edge'].append(redundant_percent_registry_with)
            if flag & Dockerhub.COMPONENT != 0:
                redundancy_list_old['component'].append(redundant_percent_old)
                redundancy_list_registry_with['component'].append(redundant_percent_registry_with)
            if flag & Dockerhub.SERVERLESS != 0:
                redundancy_list_old['serverless'].append(redundant_percent_old)
                redundancy_list_registry_with['serverless'].append(redundant_percent_registry_with)
            if flag & Dockerhub.VIDEO != 0:
                redundancy_list_old['video'].append(redundant_percent_old)
                redundancy_list_registry_with['video'].append(redundant_percent_registry_with)
        rows_old = {}
        for scenario, data_list in redundancy_list_old.items():
            rows_old[scenario] = np.mean(np.array(data_list))
        rows_registry_with = {}
        for scenario, data_list in redundancy_list_registry_with.items():
            rows_registry_with[scenario] = np.mean(np.array(data_list))
        rows = []
        for scenario in Dockerhub.scenarios():
            rows.append({
                'old': rows_old[scenario],
                'registry_with': rows_registry_with[scenario]
            })
        pd.DataFrame(rows, index=Dockerhub.scenarios()).to_csv(data_path, index=True)

    def images_to_filecount_by_path(self, data_path: str):
        images = self.__querier.images2files_group_by_field('root_path')
        rows = []
        for image, file_paths in images.items():
            rows.append({
                'image': image,
                'total_file_count': len(file_paths)
            })
        pd.DataFrame(rows).to_csv(data_path, index=False)
