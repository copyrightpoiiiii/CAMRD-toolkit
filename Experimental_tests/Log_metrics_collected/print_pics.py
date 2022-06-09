from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.ticker import MultipleLocator

line_width = "4"
label_size = 30
legent_font_size = 25
label_font_size = 35

def get_cdf(data):
    x = sorted(data.keys())
    cdf = []
    for i in range(0, x[-1] + 1):
        cdf.append(data[i])
    return cdf


def calc_cdf(data):
    x = sorted(data.keys())
    y = [data[i] for i in x]
    y = np.cumsum(y / np.sum(y))
    return x, y

def print_pic(ai_x,ai_y,online_x,online_y,sae_x,sae_y,k8s_x,k8s_y,video_x,video_y,if_log,if_auto,x_label,y_label,pic_name):
    plt.figure(figsize=(9, 7))
    plt.plot(ai_x, ai_y, label="AI", linewidth=line_width, color='royalblue', linestyle='dotted')
    plt.plot(online_x, online_y, label="Edge", linewidth=line_width, color='orange', linestyle='dashed')
    plt.plot(sae_x, sae_y, label="Serverless", linewidth=line_width, color='limegreen', linestyle='solid')
    plt.plot(k8s_x, k8s_y, label="Component", linewidth=line_width, color='pink', linestyle=(0,(3,1,1,1,1,1)))
    plt.plot(video_x, video_y, label="Video", linewidth=line_width, color='darkred', linestyle='dashdot')

    plt.legend(frameon=False, fontsize=25)

    plt.tick_params(labelsize=30)
    if if_log:
        plt.xscale("log")

    plt.xlabel(x_label, fontsize=35)
    plt.ylabel(y_label, fontsize=35)

    plt.ylim(0, 1)

    if if_auto:
        plt.axis('auto')

    plt.tight_layout()

    plt.savefig("output/"+pic_name+".pdf")
    #plt.savefig("output/"+pic_name+".eps")
    plt.close()

def pic4():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic4.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item / 1000000] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item / 1000000] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item / 1000000] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item / 1000000] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item / 1000000] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, True, 'Layer size (MB)', 'Layers', '4.layer_size')

def pic3():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic3.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item / 1000000] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item / 1000000] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item / 1000000] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item / 1000000] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item / 1000000] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, True, 'Image size (MB)', 'Images', '3.image_size')

def pic31():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic31.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Layer size (MB)', 'Requests', '32-cdf_for_layerSize_requests')

def pic32():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic32.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, True, 'Image size (MB)', 'Requests', '33-cdf_for_imageSize_requests')

def pic11():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic11.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, True, 'Number of pulls', 'Layers', '30.the_cdf_of_layer_pull_time')

def pic5():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic5.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()
    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, True, 'Number of pulls', 'Images', '5')

def pic26():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic26.txt", "r")
    lines = f.readlines()
    data = eval(lines[0])
    test_dict = {}

    for item in data:
        repo = item[0]
        time = float(item[1])
        if not repo in test_dict.keys():
            test_dict[repo] = time
        else:
            gap = time - test_dict[repo]
            sae_image_data[gap] += 1
            test_dict[repo] = time

    data = eval(lines[1])
    test_dict = {}

    for item in data:
        repo = item[0]
        time = float(item[1])
        if not repo in test_dict.keys():
            test_dict[repo] = time
        else:
            gap = time - test_dict[repo]
            ai_image_data[gap] += 1
            test_dict[repo] = time

    data = eval(lines[2])
    test_dict = {}

    for item in data:
        repo = item[0]
        time = float(item[1])
        if not repo in test_dict.keys():
            test_dict[repo] = time
        else:
            gap = time - test_dict[repo]
            online_image_data[gap] += 1
            test_dict[repo] = time

    data = eval(lines[3])
    test_dict = {}

    for item in data:
        repo = item[0]
        time = float(item[1])
        if not repo in test_dict.keys():
            test_dict[repo] = time
        else:
            gap = time - test_dict[repo]
            k8s_image_data[gap] += 1
            test_dict[repo] = time

    data = eval(lines[4])
    test_dict = {}

    for item in data:
        repo = item[0]
        time = float(item[1])
        if not repo in test_dict.keys():
            test_dict[repo] = time
        else:
            gap = time - test_dict[repo]
            video_image_data[gap] += 1
            test_dict[repo] = time

    f.close()
    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Pull interval (s)', 'Requests', '27.the_interval_for_the_same_layer_pull')


def pic25():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)
    f = open("output/pic24.txt", "r")
    lines = f.readlines()
    data = eval(lines[0])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            sae_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[1])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            ai_image_data[gap] += 1
            test_dict[(repo, tag)] = time
    
    data = eval(lines[2])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            online_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[3])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            k8s_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[4])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            video_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    f.close()
    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Pull interval (s)', 'Requests', '26.the_interval_for_the_same_image_pull')


def pic28():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic28.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item[2] - item[1]] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item[2] - item[1]] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item[2] - item[1]] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item[2] - item[1]] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item[2] - item[1]] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Pull interval (s)', 'Layers', '29.layer_first_request_last_request')

def pic8():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic8.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Pull interval (s)', 'Images', '8')

def pic29():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic29.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of nodes', 'Layers', '30-cdf_for_layer_pulled_by_node')


def pic7():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic7.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of nodes', 'Images', '7')


def pic13():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic13.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of layers', 'Nodes', '13')


def pic10():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic10.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of images', 'Nodes', '10')


def pic17():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic17.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Time interval(s)', 'Images', '18-gap_between_upload_pull')


def pic27():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic9.txt", "r")
    lines = f.readlines()
    data = eval(lines[0])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            sae_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[1])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            ai_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[2])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            online_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[3])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            k8s_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    data = eval(lines[4])
    test_dict = {}

    for item in data:
        repo = item[0]
        tag = item[1]
        time = float(item[2])
        if not (repo, tag) in test_dict.keys():
            test_dict[(repo, tag)] = time
        else:
            gap = time - test_dict[(repo, tag)]
            video_image_data[gap] += 1
            test_dict[(repo, tag)] = time

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Request interval (s)', 'Requests', '28-the_interval_for_the_same_image_request')


def pic18():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic18.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of times', 'Nodes', '19-cdf_for_node_pull_image')


def pic19():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic19.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item[1] - item[0]] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item[1] - item[0]] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item[1] - item[0]] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item[1] - item[0]] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item[1] - item[0]] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Request interval (s)', 'Nodes', '20-gap_between_upload_pull_for_node')


def pic30():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic30.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    plt.gca().xaxis.set_major_locator(MultipleLocator(5))

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, False, False, 'Number of repositories', 'Nodes', '31-cdf_for_nodes_pull_repo')


def pic22():
    f = open("output/pic21.txt", "r")
    lines = f.readlines()

    sae_image_data = eval(lines[0])

    ai_image_data = eval(lines[1])

    online_image_data = eval(lines[2])

    k8s_image_data = eval(lines[3])

    video_image_data = eval(lines[4])

    f.close()

    ai_x = np.arange(1, len(ai_image_data) + 1, 1)
    ai_cdf = sorted(ai_image_data, reverse=True)
    ai_cdf = np.cumsum(ai_cdf / np.sum(ai_cdf))

    online_x = np.arange(1, len(online_image_data) + 1, 1)
    online_cdf = sorted(online_image_data, reverse=True)
    online_cdf = np.cumsum(online_cdf / np.sum(online_cdf))

    sae_x = np.arange(1, len(sae_image_data) + 1, 1)
    sae_cdf = sorted(sae_image_data, reverse=True)
    sae_cdf = np.cumsum(sae_cdf / np.sum(sae_cdf))

    k8s_x = np.arange(1, len(k8s_image_data) + 1, 1)
    k8s_cdf = sorted(k8s_image_data, reverse=True)
    k8s_cdf = np.cumsum(k8s_cdf / np.sum(k8s_cdf))

    video_x = np.arange(1, len(video_image_data) + 1, 1)
    video_cdf = sorted(video_image_data, reverse=True)
    video_cdf = np.cumsum(video_cdf / np.sum(video_cdf))

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, False, False, 'Number of repositories', 'Requests', '23-cdf_for_repo_request')


def pic23():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic23.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, True, False, 'Number of nodes', 'Repositories', '24-cdf_for_repo_nodes')


def pic14():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic15.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, False, False, 'Number of images', 'Layers', '15-layer_in_images_cdf')


def pic15():
    sae_image_data = defaultdict(int)
    ai_image_data = defaultdict(int)
    online_image_data = defaultdict(int)
    k8s_image_data = defaultdict(int)
    video_image_data = defaultdict(int)

    f = open("output/pic16.txt", "r")
    lines = f.readlines()

    data = eval(lines[0])
    for item in data:
        sae_image_data[item] += 1

    data = eval(lines[1])
    for item in data:
        ai_image_data[item] += 1

    data = eval(lines[2])
    for item in data:
        online_image_data[item] += 1

    data = eval(lines[3])
    for item in data:
        k8s_image_data[item] += 1

    data = eval(lines[4])
    for item in data:
        video_image_data[item] += 1

    f.close()

    ai_x, ai_cdf = calc_cdf(ai_image_data)
    online_x, online_cdf = calc_cdf(online_image_data)
    sae_x, sae_cdf = calc_cdf(sae_image_data)
    k8s_x, k8s_cdf = calc_cdf(k8s_image_data)
    video_x, video_cdf = calc_cdf(video_image_data)

    print_pic(ai_x, ai_cdf, online_x, online_cdf, sae_x, sae_cdf, k8s_x, k8s_cdf, video_x, video_cdf, False, False, 'Number of repositories', 'Layers', '16-layer_in_repos_cdf')


pic4()
pic3()
pic31()
pic32()
pic11()
pic5()
pic26()
pic25()
pic28()
pic8()
pic29()
pic7()
pic13()
pic10()
pic17()
pic27()
pic18()
pic19()
pic30()
pic22()
pic23()
pic14()
pic15()