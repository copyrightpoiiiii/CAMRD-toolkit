import hashlib
from collections import defaultdict

import pymysql
import pandas as pd
import time
import os
import subprocess
import json
import sys

def Judge(state, node, con_rec, ip_rec, image_time_bar, a, w):
    gap_record = []
    if (str(state), node) in con_rec.keys():
        return bool(con_rec[(str(state), node)])
    for record in ip_rec.values():
        rec_repeat = defaultdict(bool)
        last_time = 0
        cnt = 0
        for item in record:
            if rec_repeat[item[0][0]]:
                rec_repeat.clear()
                last_time = 0
                cnt = 0
            elif item == node and cnt == len(state):
                gap_record.append(item[1] - last_time)
            if item[0][0] in state:
                rec_repeat[item[0][0]] = True
                last_time = item[1]
                cnt += 1
    gap_record = sorted(gap_record)
    max_time = 0
    for image in state:
        max_time = max(max_time, image_time_bar[image])
    result = []
    tmp = []
    for record in gap_record:
        if record <= max_time * a:
            result.append(record)
        else:
            tmp.append(record - max_time)
    if len(tmp) > 0:
        magic = tmp[int(len(tmp) * 0.1)]
        for item in gap_record:
            if item > max_time * a:
                if item <= max_time * a + magic * w:
                    result.append(item)
                else:
                    break
    if len(result) >= len(gap_record) * 0.2:
        con_rec[(str(state), node)] = True
    else:
        con_rec[(str(state), node)] = False
    return con_rec[(str(state), node)]


def dfs(node, vis, state, memory, edge, con_rec, ip_rec, image_time_bar, a, w):
    if (str(state), node) in memory.keys():
        return
    if len(state) > 0:
        if not Judge(state, node, con_rec, ip_rec, image_time_bar, a, w):
            memory[(str(state), node)] = False
            return
        memory[(str(state), node)] = True
    if not node in edge.keys():
        return
    state.append(node)
    state = sorted(state)
    if len(edge[node]) > 0:
        for v in edge[node]:
            if not vis[v]:
                vis[v] = True
                dfs(v, vis, state, memory, edge, con_rec, ip_rec, image_time_bar, a, w)


def dynamic_dependency( w, a, file_path,db_name,pwd):
    db = pymysql.connect(host="db", user="root", password=pwd,
                         database="log_aggregation")

    image_dict = defaultdict(int)
    image_pair_dict = defaultdict(dict)
    image_time_bar = defaultdict(float)
    memory = {}
    con_rec = {}
    edge = defaultdict(list)

    query = "select count(*) as num,image_repo,avg(size)/avg(speed) as time_bar from ( select image_repo,sum(response_body_length)/1000000.0 as size,sum(response_body_length)/(1000.0*sum(response_reponse_time)) as speed from "+db_name+" where request_id > 0 group by request_id,image_repo,image_tag having sum(response_reponse_time)>0) as a group by image_repo having num > 1 "
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    #print(len(results))
    for image_log in results:
        image_dict[image_log[1]] = int(image_log[0])
        image_time_bar[image_log[1]] = float(image_log[2])

    query = "select image_repo,min(request_timestamp) as pull_time,image_tag from "+db_name+" where request_id > 0  group by request_id,image_repo,image_tag order by pull_time "

    cursor.execute(query)
    results = cursor.fetchall()
    #print(len(results))
    for i in range(len(results)):
        item = results[i]
        j = i + 1
        while j < len(results):
            if results[j][1] - item[1] > 1200 :
                break
            if (results[j][0], results[j][-1]) != (item[0], item[-1]):
                if (results[j][0], results[j][-1]) in image_pair_dict[(item[0], item[-1])].keys():
                    image_pair_dict[(item[0], item[-1])][(results[j][0], results[j][-1])].append(float(results[j][1] - item[1]))
                else:
                    image_pair_dict[(item[0], item[-1])][(results[j][0], results[j][-1])] = [float(results[j][1] - item[1])]
            j += 1
    ip_rec = {}
    ip_rec['0'] = results

    #print("get")
    f = open(file_path , "w+")

    cnt = 0
    sum = 0

    for k in image_pair_dict.keys():
        for image in image_pair_dict[k].keys():
            if len(image_pair_dict[k][image]) < 5:
                continue
            image_pair_dict[k][image] = sorted(image_pair_dict[k][image])
            tmp = []
            result = []
            cnt_size = 0
            for item in image_pair_dict[k][image]:
                if item <= 1200.0:
                    cnt_size += 1
                if item > image_time_bar[k] * a:
                    tmp.append(item - image_time_bar[k])
                else:
                    result.append(item)
            if len(tmp) > 0:
                magic = tmp[int(len(tmp) * 0.1)]
                for item in image_pair_dict[k][image]:
                    if item > image_time_bar[k] * a:
                        if item <= image_time_bar[k] * a + magic * w:
                            result.append(item)
                        else:
                            break
            if len(result) < len(image_pair_dict[k][image]) * 0.2:
                result = []
            if len(result) > 0:
                sum += len(result)
                print((k, image), file=f)
                if not (k, image) in con_rec.keys():
                    edge[k].append(image)
                    con_rec[(k, image)] = 1
                    cnt += 1
    #print(sum)
    f.close()
    for k in con_rec.keys():
        mirror_con = (k[1], k[0])
        if mirror_con in con_rec.keys() and con_rec[mirror_con] == 1:
            con_rec[mirror_con] = 0
        con_rec[k] = 0

    #print("start dfs!")
    for u in edge.keys():
        vis = defaultdict(bool)
        vis[u] = True
        dfs(u, vis, [], memory, edge, con_rec, ip_rec, image_time_bar, a, w)

    result = []
    #print(len(memory.keys()))
    for (k, v) in memory.items():
        if v == True:
            tmp = eval(k[0])
            tmp.append(k[1])
            result.append(sorted(tmp))
    result = sorted(result, key=lambda x: len(x), reverse=True)
    return result

def main():
    file_name = sys.argv[1]
    f = open(file_name, "w+")
    res = dynamic_dependency( 1.5, 2, sys.argv[2], sys.argv[3], sys.argv[4])
    #print(len(res))
    for item in res:
        print(item, file=f)

if __name__ == '__main__':
    main()
