#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dockerhub import Dockerhub

class Plot:
    
    def __init__(self) -> None:
        pass

    def file_redundancy(self, data_path: str, figure_path: str):
        df = pd.read_csv(data_path)
        x_labels = ['AI', 'Edge', 'Serverless', 'Component', 'Video']
        x = np.arange(len(x_labels))
        plt.figure(figsize=(8, 3))
        width = 0.3
        linewidth = '2'
        plt.bar(x, df['old'], width=width, linewidth=linewidth, label='In repo', edgecolor='black', hatch='\\')
        plt.bar(x + width, df['registry_with'], width=width, linewidth=linewidth, label='In registry', edgecolor='black', hatch='+')
        plt.xticks(x + width / 2, x_labels, fontsize=15)
        plt.ylabel('Redundancy', fontsize=20)
        plt.legend(frameon=False, fontsize=15, ncol=2)
        plt.tick_params(labelsize=15)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def accessed_file_proportion(self, accessed_file_path: str, full_file_path: str, figure_path: str):
        images_accessed_file = {}
        for row in pd.read_csv(accessed_file_path).itertuples():
            repo = str(getattr(row, 'image')) + ':' + str(getattr(row, 'tag'))
            filepath = str(getattr(row, 'filepath'))
            if repo not in images_accessed_file:
                images_accessed_file[repo] = []
            images_accessed_file[repo].append(filepath)

        images_full_file = {}
        for row in pd.read_csv(full_file_path).itertuples():
            images_full_file[str(getattr(row, 'image'))] = int(getattr(row, 'total_file_count'))

        rows = []
        for image, file_paths in images_accessed_file.items():
            total = images_full_file[image] if image in images_full_file else 0.5
            ratio = len(file_paths) / total
            if ratio <= 1:
                rows.append(ratio)

        data = np.array(sorted(rows))
        plt.figure(figsize=(9, 7))
        plt.plot(np.arange(len(data[-102:])), data[-102:], linewidth=5, color='royalblue')
        plt.tick_params(labelsize=30)
        plt.ylabel('File usage', fontsize=35)
        plt.xlabel('Images', fontsize=35)
        plt.xlim(-2, 102)
        plt.ylim(-0.03, 1)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def accessed_file_type(self, data_path: str, figure_path: str):

        def one_scenario(scenario: str, FLAG):
            repo2flag = Dockerhub.repotscenario() if FLAG == Dockerhub.AI else Dockerhub.repo2scenario()
            df = pd.read_csv(data_path)
            suffix2count = {}
            total_count = 0
            for row in df.itertuples():
                suffixes = str(getattr(row, 'filepath')).lower().split('/')[-1].split('.')
                idx = len(suffixes) - 1
                while idx >= 0 and suffixes[idx].isdigit():
                    idx -= 1
                file_suffix = suffixes[max(0, idx)]
                flag = repo2flag[str(getattr(row, 'image'))]
                if Dockerhub.scenario2flag(scenario) & flag != FLAG:
                    continue
                if file_suffix not in suffix2count:
                    suffix2count[file_suffix] = 0
                t = int(row[7])
                suffix2count[file_suffix] += t
                total_count += t
            sorted_suffix2count = sorted(suffix2count.items(), key=lambda x: x[1], reverse=True)
            suffix, percentage = [], []
            for s, c in sorted_suffix2count:
                suffix.append(s)
                percentage.append(c / total_count)
                suffix2count[s] = c / total_count
            return suffix2count, suffix, percentage

        data_ai = one_scenario('ai', Dockerhub.AI)
        data_edge = one_scenario('edge', Dockerhub.EDGE)
        data_k8s = one_scenario('component', Dockerhub.COMPONENT)
        data_serveless = one_scenario('serverless', Dockerhub.SERVERLESS)
        data_vedio = one_scenario('video', Dockerhub.VIDEO)

        top = 10
        x = data_serveless[1][:top]
        y_serverless = data_serveless[2][:top]
        y_ai = [data_ai[0].get(suffix, 0) for suffix in x]
        y_edge = [data_edge[0].get(suffix, 0) for suffix in x]
        y_k8s = [data_k8s[0].get(suffix, 0) for suffix in x]
        y_vedio = [data_vedio[0].get(suffix, 0) for suffix in x]

        plt.figure(figsize=(9, 7))
        plt.plot(x, y_ai, linewidth='5', label='AI', color='royalblue', linestyle='dotted')
        plt.plot(x, y_edge, linewidth='5', label='Edge', color='orange', linestyle='dashed')
        plt.plot(x, y_serverless, linewidth='5', label='Serverless', color='limegreen', linestyle='solid')
        plt.plot(x, y_k8s, linewidth='5', label='Component', color='pink', linestyle=(0,(3,1,1,1,1,1)))
        plt.plot(x, y_vedio, linewidth='5', label='Video', color='darkred', linestyle='dashdot')
        plt.xticks(rotation=55)
        plt.ylabel('File size', fontsize=35)
        plt.legend(frameon=False, fontsize=25)
        plt.tick_params(labelsize=30)
        plt.ylim(-0.03, 0.6)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def accessed_file_in_layer(self, data_path: str, figure_path: str):
        df = pd.read_csv(data_path)
        data = df['file_layer'] / df['total_layers']
        hist, bins = np.histogram(data, bins=100)
        cdf = np.cumsum(hist / np.sum(hist))
        plt.figure(figsize=(9, 7))
        plt.plot(bins[1:], cdf, linewidth='5', color='royalblue')
        plt.ylabel('File count', fontsize=35)
        plt.xlabel('Layer where a file access / total layers', fontsize=29, labelpad=20)
        plt.tick_params(labelsize=30)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def accessed_file_redundancy(self, data_path: str, figure_path: str):
        df = pd.read_csv(data_path)
        images = {}
        for row in df.itertuples():
            repo = str(getattr(row, 'image'))
            tag = str(getattr(row, 'tag'))
            filepath = str(getattr(row, 'filepath'))
            if repo not in images:
                images[repo] = {}
            if tag not in images[repo]:
                images[repo][tag] = {}
            if filepath not in images[repo][tag]:
                images[repo][tag][filepath] = 0
            images[repo][tag][filepath] += 1
        redundants = {}
        for repo, tags_info in images.items():
            versions = tags_info.keys()
            if len(versions) != 2:
                continue
            total_cnt, redundancy_cnt = 0, 0
            new_tag, old_tag = versions
            for path, cnt in tags_info[new_tag].items():
                if path in tags_info[old_tag]:
                    redundancy_cnt += cnt
                total_cnt += cnt
            redundants[repo] = redundancy_cnt / total_cnt
        ai, edge, serverless, component, video = [], [], [], [], []
        repo2flag = Dockerhub.repo2scenario()
        for repo, redundancy in redundants.items():
            flag = repo2flag[repo]
            if flag & Dockerhub.AI != 0:
                ai.append(redundancy)
            if flag & Dockerhub.EDGE != 0:
                edge.append(redundancy)
            if flag & Dockerhub.SERVERLESS != 0:
                serverless.append(redundancy)
            if flag & Dockerhub.COMPONENT != 0:
                component.append(redundancy)
            if flag & Dockerhub.VIDEO != 0:
                video.append(redundancy)
        x_labels = ['AI', 'Edge', 'Serverless', 'Component', 'Video']
        y = [
            np.mean(np.array(ai)), np.mean(np.array(edge)),
            np.mean(np.array(serverless)), np.mean(np.array(component)),
            np.mean(np.array(video))
        ]
        plt.figure(figsize=(9, 7))
        plt.bar(np.arange(len(x_labels)), y, linewidth='1', width=0.4, edgecolor='black', color='royalblue')
        plt.xticks(np.arange(len(x_labels)), x_labels,fontsize=30, rotation=10)
        plt.ylabel('Redundancy', fontsize=30)
        plt.tick_params(labelsize=25)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def accessed_file_shared(self, data_path: str, figure_path: str):
        df = pd.read_csv(data_path)
        x = df['filepath'].value_counts(ascending=True) - 1
        y = np.arange(0, 1, 1 / len(x))
        plt.figure(figsize=(9, 7))
        plt.plot(x, y, linewidth='5', color='royalblue')
        plt.ylabel('Ratio', fontsize=35)
        plt.xlabel('Sharing count', fontsize=29, labelpad=20)
        plt.tick_params(labelsize=30)
        plt.ylim(0, 1.01)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()
    
    def container_running(self, data_path: str, figure_path: str):
        return
        df = pd.read_csv(data_path)
        df['size(byte)'] = df['size(byte)'] / np.sum(df['size(byte)'])
        progress = 0
        tradition, dadi5, dadi10, dadi100 = 0, 0, 0, 0
        progress_list = []
        tradition_list, dadi5_list, dadi10_list, dadi100_list = [], [], [], []
        for row in df.itertuples():
            progress += float(row[3])
            tradition += float(row[4])
            dadi5 += float(row[5])
            dadi10 += float(row[6])
            dadi100 += float(row[7])
            if progress > 0.08:
                progress_list.append(progress)
                tradition_list.append(tradition)
                dadi5_list.append(dadi5)
                dadi10_list.append(dadi10)
                dadi100_list.append(dadi100)
                progress = 0
                tradition, dadi5, dadi10, dadi100 = 0, 0, 0, 0
        progress_list.append(progress)
        tradition_list.append(tradition)
        dadi5_list.append(dadi5)
        dadi10_list.append(dadi10)
        dadi100_list.append(dadi100)
        tradition_list = np.array(tradition_list) / 1e6
        dadi5_list = np.array(dadi5_list) / 1e6
        dadi10_list = np.array(dadi10_list) / 1e6
        dadi100_list = np.array(dadi100_list) / 1e6
        tradition_list = [0] + list(tradition_list)
        dadi5_list = [0] + list(dadi5_list)
        dadi10_list = [0] + list(dadi10_list)
        dadi100_list = [0] + list(dadi100_list)
        x = np.arange(len(progress_list) + 1)
        line_width = 5
        plt.figure(figsize=(9, 7))
        plt.plot(x, tradition_list, label="Traditional", linewidth=line_width, color='limegreen', linestyle='dashdot')
        plt.plot(x, dadi5_list, label="DADI-5M", linewidth=line_width, color='pink', linestyle=(0, (3, 1, 1, 1, 1, 1)))
        plt.plot(x, dadi10_list, label="DADI-10M", linewidth=line_width, color='darkred', linestyle='dashed')
        plt.plot(x, dadi100_list, label="DADI-100M", linewidth=line_width, color='red', linestyle='dotted')
        from matplotlib.ticker import FuncFormatter
        def to_percent(temp, position):
            return '%1.0f'%(10*temp) + '%'
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.xlim(0, 10)
        plt.ylim(-0.2, 6)
        plt.legend(frameon=False, fontsize=25)
        plt.ylabel('Ratio', fontsize=35)
        plt.xlabel('Sharing count', fontsize=29, labelpad=20)
        plt.tick_params(labelsize=30)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()

    def four_phase(self, data_path: str, figure_path: str):
        pass

    def conversion_size(self, data_path:str, figure_path: str):
        df = pd.read_csv(data_path, sep=' ')
        tradition, ondemand = df['tradition'], df['on_demand']
        times = ondemand / tradition
        k1, k2 = np.min(times), np.max(times)
        k, b = np.polyfit(tradition, ondemand, 1)
        x = np.arange(np.max(tradition))
        plt.figure(figsize=(9, 7))
        plt.scatter(tradition, ondemand, color='#014686', marker='o', edgecolor='#014686', s=50, label='image')
        plt.text(500, 500, '$y=%.2fx$' %k1, fontsize=25)
        plt.plot(x, k1 * x, linewidth='3', color='#9f9f9f', linestyle='dotted',  dashes=(1, 1))
        plt.text(250, 1000, '$y=%.2fx$' %k2, fontsize=25)
        plt.plot(x, k2 * x, linewidth='3', color='#9f9f9f', linestyle='dotted',  dashes=(1, 1))
        plt.xlabel('Traditional image size (MB)', fontsize=35)
        plt.ylabel('On-demand image\nsize (MB)', fontsize=35)
        plt.tick_params(labelsize=30)
        plt.tight_layout()
        plt.savefig(figure_path)
        plt.close()
