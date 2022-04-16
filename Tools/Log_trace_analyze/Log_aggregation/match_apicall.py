import os
from collections import defaultdict

import pandas as pd
import math
import bisect


def match_blob(target, rec, time_gap):
    time_gap = max(time_gap, 60)
    if rec[4] in target.keys():
        pos = bisect.bisect_left(target[rec[4]][1], math.floor(float(rec[0])) - 1)
        leng = len(target[rec[4]][0])
        if rec[5] == 'Internet':
            while pos < leng:
                if abs(target[rec[4]][1][pos] - rec[0]) > time_gap:
                    break
                if target[rec[4]][0][pos][-2] == rec[-2] and target[rec[4]][0][pos][-1] == -1 and target[rec[4]][0][pos][3] == 'Internet':
                    target[rec[4]][0][pos][-1] = rec[-1]
                    break
                pos += 1
        else:
            while pos < leng:
                if abs(target[rec[4]][1][pos] - rec[0]) > time_gap:
                    break
                if target[rec[4]][0][pos][-2] == rec[-2] and target[rec[4]][0][pos][-1] == -1 and \
                        target[rec[4]][0][pos][3] == 'Interval':
                    target[rec[4]][0][pos][-1] = rec[-1]
                    break
                pos += 1

def match_nomanifest_log(image, tag, blob_request, object_request, manifest_request):

    internal_obj = []
    inter_obj = []
    for item in blob_request:
        if item[-1] > 0:
            continue
        if item[5] == "Interval":
            internal_obj.append(item)
        else:
            inter_obj.append(item)

    internal_getobject_obj = defaultdict(list)
    inter_getobject_obj = defaultdict(list)

    for item in object_request:
        if item[-1] > 0:
            continue
        if item[3] == "Interval":
            internal_getobject_obj[item[2]].append(item)
        else:
            inter_getobject_obj[item[2]].append(item)

    internal_manifest = []
    inter_manifest = []
    for item in manifest_request:
        if item[-1] > 0:
            continue
        if item[5] == "Interval":
            internal_manifest.append(item)
        else:
            inter_manifest.append(item)

    internal_result = match_manifest(image, tag, internal_obj, internal_getobject_obj, internal_manifest)
    inter_result = match_manifest(image, tag, inter_obj, inter_getobject_obj, inter_manifest)

    return internal_result + inter_result



def match_manifest(image, tag, obj, getobject_obj, manifest_request):
    config = open("env.config", "r")
    cnt = int(config.read())
    config.close()

    for k, v in getobject_obj.items():
        v = sorted(v, key=lambda x: x[0])
        getobject_obj[k] = (v, [float(i[0]) for i in v])

    manifest_request = sorted(manifest_request, key=lambda x: x[0])

    obj = sorted(obj, key=lambda x: x[0])
    blob_time = [i[0] for i in obj]

    for i in range(len(manifest_request)):
        rec = manifest_request[i]
        pos = bisect.bisect_left(blob_time, rec[0])
        digest_dict = defaultdict(int)
        while pos < len(obj):
            if abs(obj[pos][0] - rec[0]) > 60:
                break
            if obj[pos][-1] != -1:
                pos += 1
                continue
            if digest_dict[obj[pos][4]] == 1:
                pos += 1
                continue
            if rec[5] == obj[pos][5] and rec[-2] == obj[pos][-2]:
                if rec[-1] == -1:
                    cnt += 1
                    rec[-1] = cnt
                obj[pos][-1] = rec[-1]
                digest_dict[obj[pos][4]] = 1
                match_blob(getobject_obj, obj[pos], 10)
            pos += 1
        manifest_request[i] = rec
    out = []
    result = []
    out.extend(obj)
    out.extend(manifest_request)
    for v in getobject_obj.values():
        out.extend(v[0])
    for item in out:
        if item[-1] > 0:
            result.append(item)
        elif item[1] == 'Manifest':
            result.append(item)
    config = open("env.config", "w+")
    print(cnt, file=config)
    config.close()
    return result
