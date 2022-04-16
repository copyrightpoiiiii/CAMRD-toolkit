import hashlib
from collections import defaultdict

import pymysql
import pandas as pd
import time
import os
import subprocess
import json
import sys


global image_rec, con_rec, vis, memory, edge
image_rec = defaultdict(list)
con_rec = {}
vis = defaultdict(bool)
memory = {}
edge = defaultdict(list)

def dfs(node, state, image_time_bar, a, w):
    global image_rec, con_rec, vis, memory, edge
    if node in state:
        return
    state.append(node)
    state = sorted(state)
    if str(state) in memory.keys():
        return
    if len(state) > 1:
        memory[str(state)] = True
    if not node in edge.keys():
        return
    if len(edge[node]) > 0:
        for v in edge[node]:
            if not vis[v]:
                vis[v] = True
                dfs(v, state, image_time_bar, a, w)


def dynamic_dependency(w, a, file_path, db_name, repo):
    global image_rec, con_rec, memory, edge
    image_rec = defaultdict(list)
    con_rec = {}
    memory = {}
    edge = defaultdict(list)
    image_dict = defaultdict(int)
    image_pair_dict = defaultdict(dict)
    image_time_bar = defaultdict(float)

    query = "select count(*) as num, image_tag, max(down_time) as time_bar from (select image_tag, sum(response_reponse_time)/1000.0 as down_time from "+db_name+" " \
            "where request_id > 0 and image_repo = '" + repo + "' group by request_id, image_tag) as a group by image_tag"
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    #print(len(results))
    for image_log in results:
        image_dict[image_log[1]] = int(image_log[0])
        image_time_bar[image_log[1]] = max(float(image_log[2]), 150)

    query = "select image_tag,request_timestamp as pull_time from "+db_name+" where request_api = 'Manifest' and image_repo = '" + repo + "' order by pull_time"

    cursor.execute(query)
    results = cursor.fetchall()
    #print(len(results))
    for i in range(len(results)):
        item = results[i]
        j = i + 1
        while j < len(results):
            if results[j][1] - item[1] > 10:
                break
            if results[j][0] != item[0]:
                if results[j][0] in image_pair_dict[item[0]].keys():
                    image_pair_dict[item[0]][results[j][0]].append(float(results[j][1] - item[1]))
                else:
                    image_pair_dict[item[0]][results[j][0]] = [float(results[j][1] - item[1])]
            j += 1
        image_rec[item[0]].append(item)

    #print("get")
    f = open(file_path + "pair.info", "a+")

    cnt = 0

    for k in image_pair_dict.keys():
        for image in image_pair_dict[k].keys():
            if len(image_pair_dict[k][image]) < 10:
                continue
            image_pair_dict[k][image] = sorted(image_pair_dict[k][image])
            tmp = []
            result = []
            cnt_size = 0
            for item in image_pair_dict[k][image]:
                if item <= 600.0:
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
                print(str(k) + " -> " + str(image), file=f)
                print(image_time_bar[k], file=f)
                if not (k, image) in con_rec.keys():
                    edge[k].append(image)
                    con_rec[(k, image)] = 1
                    cnt += 1
    print(cnt, file=f)
    f.close()
    for k in con_rec.keys():
        mirror_con = (k[1], k[0])
        if mirror_con in con_rec.keys() and con_rec[mirror_con] == 1:
            con_rec[mirror_con] = 0
        con_rec[k] = 0

    #print("start dfs!")
    #print(len(edge.keys()))
    for u in edge.keys():
        global vis
        vis = defaultdict(bool)
        vis[u] = True
        dfs(u, [], image_time_bar, a, w)
    #print('end dfs!')
    #print(len(memory.keys()))
    res = []
    for k in memory.keys():
        combination = json.loads(str(k).replace("'", '"'))
        cnt = 0
        silde = [0 for i in range(len(combination))]
        while 1:
            # find min time slide
            min_time_slide = 99999999999
            max_time_slide = 0
            min_pos = 0
            for i in range(len(combination)):
                item = combination[i]
                if image_rec[item][silde[i]][1] < min_time_slide:
                    min_time_slide = image_rec[item][silde[i]][1]
                    min_pos = i
                max_time_slide = max (max_time_slide, image_rec[item][silde[i]][1])
            if max_time_slide - min_time_slide <= 10:
                cnt += 1
                flag = 0
                for i in range(len(combination)):
                    silde[i] += 1
                    if silde[i] >= len(image_rec[combination[i]]):
                        flag = 1
                        break
                if flag:
                    break
            else:
                silde[min_pos] += 1
                if silde[min_pos] >= len(image_rec[combination[min_pos]]):
                    break

        min_prob = 1.0
        if cnt >= 5:
            for item in combination:
                min_prob = min(min_prob, float(cnt) / len(image_rec[item]))
            res.append((combination, min_prob, cnt, cnt))
    return res

def main():
    global db
    db = pymysql.connect(host="db", user="root", password=sys.argv[1],
                        database="log_aggregation")

    query = "select distinct image_repo from "+sys.argv[2]+" limit 300000"

    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    for repo in results:
        f = open(sys.argv[3], "a+")
        print(repo[0], file=f)
        res = dynamic_dependency(1.5, 2, repo[0]+'_', sys.argv[2], repo[0])
        #print(len(res))
        for item in res:
            print(item, file=f)
        f.close()

if __name__ == '__main__':
    main()
