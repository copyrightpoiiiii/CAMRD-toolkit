from collections import defaultdict
import sqlalchemy
import pymysql
import pandas as pd
import json
import subprocess
import sys
import hashlib
from match_apicall import match_nomanifest_log
import urllib


def is_json(testJson):
    try:
        json_storage = json.loads(testJson)
    except ValueError as e:
        return False
    return True


def manifest2tuple(data):
    return [data['timestamp'], data['api'], data['namespace'], data['repo'],
            data['tag'], data['network_type'], data['ip'], data['method'], data['user_agent'], int(-1)]


def blob2tuple(data):
    return [data['timestamp'], data['api'], data['namespace'], data['repo'], data['digest_id'], data['network_type'],
            data['ip'], data['method'], data['user_agent'], int(-1)]


def storage2tuple(data):
    return [data['timestamp'], data['api'], data['digest_id'], data['network_type'],
            data['ip'], data['method'], int(data['size']), int(data['body_length']), float(data['response_time']),
            data['user_agent'], int(-1)]


def filter_l(data, image):
    return {k: v for k, v in data.items() if k[0] == image}


def log_aggregate(manifest, blob, storage, namespace, pwd):
    pwd = urllib.parse.quote(pwd)
    con = sqlalchemy.create_engine('mysql+pymysql://root:'+pwd+'@db/log_aggregation')
    sql_columns = ['image_namespace', 'image_repo', 'image_tag', 'layer_digest_id', 'layer_size', 'request_id', 'request_method', 'request_timestamp', 'request_ip', 'request_user_agent', 'request_api', 'request_network_type', 
                   'response_body_length',  'response_reponse_time']
    Manifest_rec = defaultdict(list)
    Blob_rec = defaultdict(list)
    image_dict = defaultdict(bool)

    print("start get manifest")
    for data in manifest:
        image_dict[(data['repo'], data['tag'])] = True
        Manifest_rec[(data['repo'], data['tag'])].append(manifest2tuple(data))

    print("start get blob")
    for data in blob:
        Blob_rec[(data['repo'], data['digest_id'])].append(blob2tuple(data))


    print("start get storage")
    Storage_rec = defaultdict(list)
    for data in storage:
        Storage_rec[data['digest_id']].append(storage2tuple(data))

    print("start analysis")

    log_array = []
    for item in image_dict.keys():
        image = item[0]
        tag = item[1]
        print(image, tag)

        manifest_request = Manifest_rec[(image, tag)]
        blob_request = []
        storage_request = []

        blob_dict = filter_l(Blob_rec, image)
        for item in blob_dict.values():
            blob_request += item
        for v in blob_dict.keys():
            storage_request += Storage_rec[v[1]]
        print(len(blob_request))
        print(len(storage_request))
        #print(len(manifest_request))
        result = match_nomanifest_log(image, tag, blob_request, storage_request, manifest_request)

        for item in result:
            if item[1] == 'Object':
                log = [namespace, image, tag, item[2], item[-5], item[-1], item[5], item[0], item[4], item[-2], item[1], item[3], item[-4], item[-3]]
            elif item[1] == 'Blob':
                log = [item[2], item[3], tag, item[4], 0, item[-1], item[-3], item[0], item[-4], item[-2], item[1], item[5], 0, 0]
            else:
                log = [item[2], item[3], item[4], 'null', 0, item[-1], item[-3], item[0], item[-4], item[-2], item[1], item[5], 0, 0]
            log_array.append(log)
            if len(log_array) > 50000:
                testdf = pd.DataFrame(log_array, columns=sql_columns)
                testdf.to_sql(namespace, con, index=False, if_exists='append')
                log_array = []
    print(len(log_array))
    if len(log_array) > 0:
        testdf = pd.DataFrame(log_array, columns=sql_columns)
        testdf.to_sql(namespace, con, index=False, if_exists='append')


def main():
    file_path = 'Log_trace/'
    file_list = ['ai', 'component', 'edge', 'serverless', 'video']

    
    conn = pymysql.connect(host='db',user='root',password='12345',charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("create database if not exists log_aggregation")

    for file in file_list:
        f = open(file_path + file + '_sample.json', "r")
        requests = json.load(f)
        Manifests = []
        Blobs = []
        Storages = []
        for request in requests:
            if request['api'] == 'Manifest':
                Manifests.append(request)
            elif request['api'] == 'Blob':
                Blobs.append(request)
            else:
                Storages.append(request)
        log_aggregate(Manifests, Blobs, Storages, file, '12345')

if __name__ == '__main__':
    main()