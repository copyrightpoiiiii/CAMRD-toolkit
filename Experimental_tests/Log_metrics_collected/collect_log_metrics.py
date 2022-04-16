import pandas as pd
import sys
import time
import pymysql


    
def query_log(query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def pic1(db):
    query = "select sum(response_body_length) as layer_size,min(request_timestamp) as request_timestamp from "+db+" where request_id > 0 and request_api = 'Object' group by request_id order by request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        request_timestamp = float(data[1])
        layer_size = int(data[0])
        out_data.append((layer_size,request_timestamp))

    f = open("output/pic1.txt","a+")
    print(out_data,file=f)
    f.close()

def pic3_1(db):
    query = "select max(layer_size) as layer_size from (select image_repo,image_tag,sum(response_body_length) as layer_size from "+db+" where request_id>0 group by image_repo,image_tag,request_id) as a group by image_repo,image_tag"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[0])
        out_data.append(layer_size)
    
    f = open("output/pic3_1.txt","a+")
    print(out_data,file=f)
    f.close()

def pic3(db):
    query = "select image_repo,image_tag,max(layer_size) as layer_size from "+db+" where request_api = 'Manifest' group by image_repo,image_tag"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[2])
        out_data.append(layer_size)
    
    f = open("output/pic3.txt","a+")
    print(out_data,file=f)
    f.close()

def pic4(db):
    query = "select max(layer_size) as layer_size from "+db+" group by layer_digest_id order by layer_size"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[0])
        out_data.append(layer_size)
    
    f = open("output/pic4.txt","a+")
    print(out_data,file=f)
    f.close()

def pic5(db):
    query = "select count(distinct request_id) as num from "+db+" where request_id > 0 group by image_repo,image_tag order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[0])
        out_data.append(layer_size)

    f = open("output/pic5.txt","a+")
    print(out_data,file=f)
    f.close()

def pic7(db):
    query = "select count(distinct request_id) as num,count(distinct request_ip) as ip_num from "+db+" where request_id > 0 and request_api = 'Object' group by image_repo,image_tag having num >= 5 order by ip_num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[1])
        out_data.append(layer_size)
    
    f = open("output/pic7.txt","a+")
    print(out_data,file=f)
    f.close()


def pic8(db):
    query = "select count(distinct request_id) as num,min(request_timestamp) as f_time,max(request_timestamp) as l_time from "+db+" where request_id > 0 group by image_repo,image_tag having num >= 5"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        f_time = float(data[1])
        l_time = float(data[2])
        out_data.append(l_time-f_time)
    
    f = open("output/pic8.txt","a+")
    print(out_data,file=f)
    f.close()


def pic9(db):
    query = "select b.image_repo as image_repo,b.image_tag as image_tag,request_timestamp from "+db+" as b join (select count(distinct request_id) as num,image_repo,image_tag from "+db+" where request_id > 0 group by image_repo,image_tag having num >= 5) as a on a.image_tag = b.image_tag and a.image_repo = b.image_repo where request_api = 'Manifest' order by request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        image_repo = data[0]
        image_tag = data[1]
        request_timestamp =float(data[2])
        out_data.append((image_repo,image_tag,request_timestamp))

    f = open("output/pic9.txt","a+")
    print(out_data,file=f)
    f.close()


def pic10(db):
    query = "select sum(num) as num from (select b.request_ip,count(distinct b.image_tag) as num from "+db+" as b join (select count(distinct request_id) as num,image_repo,image_tag from "+db+" where request_id > 0 group by image_repo,image_tag having num >= 5) as a on a.image_tag = b.image_tag and a.image_repo = b.image_repo where request_id > 0 and request_api = 'Object' group by b.request_ip,b.image_repo) as c group by request_ip order by num desc"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = int(data[0])
        out_data.append(num)

    f = open("output/pic10.txt","a+")
    print(out_data,file=f)
    f.close()


def pic11(db):
    query = "select count(*) as num from "+db+" group by layer_digest_id order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = int(data[0])
        out_data.append(num)

    f = open("output/pic11.txt","a+")
    print(out_data,file=f)
    f.close()


def pic12(db):
    query = "select a.layer_digest_id as a,request_timestamp from "+db+" as b join (select count(*) as num,layer_digest_id from "+db+" group by layer_digest_id having num >= 10) as a on a.layer_digest_id = b.layer_digest_id order by request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_digest_id = data[0]
        request_timestamp = data[1]
        out_data.append((layer_digest_id,request_timestamp))
    f = open("output/pic12.txt","a+")
    print(out_data,file=f)
    f.close()


def pic13(db):
    query = "select count(distinct a.layer_digest_id) as num from "+db+" as b join (select count(*) as num,layer_digest_id from "+db+" group by layer_digest_id having num >= 10) as a on a.layer_digest_id = b.layer_digest_id group by request_ip order by num desc"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic13.txt","a+")
    print(out_data,file=f)
    f.close()

def pic14(db):
    query = "select sum(num) as num from ( select layer_digest_id,count(distinct image_tag) as num from "+db+" where request_api = 'Blob' group by layer_digest_id,image_repo) as a group by layer_digest_id order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic14.txt","a+")
    print(out_data,file=f)
    f.close()


def pic15(db):
    query = "select count(distinct image_repo) as num from "+db+" where request_api = 'Blob' group by layer_digest_id order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic15.txt","a+")
    print(out_data,file=f)
    f.close()


def pic16(db):
    query = "select count(*) as num from "+db+" where request_api = 'Manifest' group by image_repo,image_tag order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic16.txt","a+")
    print(out_data,file=f)
    f.close()


def pic17(db):
    query = "select b.request_timestamp-a.upload_time as gap from (select image_repo,image_tag,min(request_timestamp) as request_timestamp from "+db+" where request_api = 'Manifest' group by image_repo, image_tag) as b join (select image_repo,image_tag,min(request_timestamp) as upload_time from "+db+" where request_api = 'PutImageManifest' group by image_repo, image_tag) as a on b.image_repo = a.image_repo and b.image_tag = a.image_tag and b.request_timestamp > a.upload_time order by gap desc"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = float(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic17.txt","a+")
    print(out_data,file=f)
    f.close()

def pic18(db):
    query = "select count(distinct request_id) as num from "+db+" where request_id > 0 and request_api = 'Object' group by request_ip order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic18.txt","a+")
    print(out_data,file=f)
    f.close()

def pic19(db):
    query = "select min(request_timestamp) as f_time,max(request_timestamp) as t_time from "+db+" where request_id > 0 and request_api = 'Object' group by request_ip"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        f_time = float(data[0])
        t_time = float(data[1])
        out_data.append((f_time,t_time))
    f = open("output/pic19.txt","a+")
    print(out_data,file=f)
    f.close()


def pic20(db):
    query = "select request_timestamp from "+db+" where request_api = 'Manifest' order by request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = float(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic20.txt","a+")
    print(out_data,file=f)
    f.close()

def pic21(db):
    query = "select count(*) as num from "+db+" where request_api = 'Manifest' group by image_repo"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic21.txt","a+")
    print(out_data,file=f)
    f.close()


def pic23(db):
    query = "select count(distinct request_ip) as num from "+db+" where request_api = 'Object' group by image_repo"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        request_timestamp = int(data[0])
        out_data.append(request_timestamp)
    f = open("output/pic23.txt","a+")
    print(out_data,file=f)
    f.close()

def pic24(db):
    query = "select b.image_repo as image_repo,b.image_tag as image_tag,request_timestamp from "+db+" as b join (select count(distinct request_id) as num,image_repo,image_tag from "+db+" where request_id > 0 group by image_repo,image_tag having num >= 5) as a on a.image_tag = b.image_tag and a.image_repo = b.image_repo where request_id > 0 and request_api = 'Manifest' order by request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        image_repo = data[0]
        image_tag = data[1]
        request_timestamp =float(data[2])
        out_data.append((image_repo,image_tag,request_timestamp))

    f = open("output/pic24.txt","a+")
    print(out_data,file=f)
    f.close()

def pic26(db):
    query = "select a.layer_digest_id as d,request_timestamp from "+db+" as b join (select count(*) as num,layer_digest_id from "+db+" group by layer_digest_id having num >= 10) as a on a.layer_digest_id = b.layer_digest_id order by b.request_timestamp"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        image_repo = data[0]
        request_timestamp = data[1]
        out_data.append((image_repo,request_timestamp))

    f = open("output/pic26.txt","a+")
    print(out_data,file=f)
    f.close()

def pic28(db):
    query = "select count(*) as num,min(request_timestamp) as f_time,max(request_timestamp) as l_time from "+db+" group by layer_digest_id  having num >= 10"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = int(data[0])
        f_time = request_timestamp = data[1]
        l_time = request_timestamp = data[2]
        out_data.append((num, f_time, l_time))

    f = open("output/pic28.txt","a+")
    print(out_data,file=f)
    f.close()

def pic29(db):
    query = "select count(*) as num,count(distinct request_ip) as ip_num from "+db+" group by layer_digest_id having num >= 10 order by ip_num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = int(data[1])
        out_data.append(num)

    f = open("output/pic29.txt","a+")
    print(out_data,file=f)
    f.close()

def pic30(db):
    query = "select count(distinct image_repo) as num from "+db+" where request_api = 'Object' group by request_ip order by num"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = int(data[0])
        out_data.append(num)

    f = open("output/pic30.txt","a+")
    print(out_data,file=f)
    f.close()

def pic31(db):
    query = "select response_body_length/1000000.0 as num from "+db
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = float(data[0])
        out_data.append(num)

    f = open("output/pic31.txt","a+")
    print(out_data,file=f)
    f.close()

def pic32(db):
    query = "select sum(response_body_length)/1000000.0 as num from "+db+" where request_id > 0 group by request_id"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        num = float(data[0])
        out_data.append(num)

    f = open("output/pic32.txt","a+")
    print(out_data,file=f)
    f.close()

def pic33(db):
    query = "select sum(response_body_length) as layer_size,sum(response_reponse_time) as request_timestamp from "+db+" where request_id > 0 and request_api = 'Object' group by request_id"
    logs = query_log(query)
    out_data = []

    for data in logs:
        
        layer_size = int(data[0])
        request_timestamp = float(data[1])
        out_data.append((layer_size,request_timestamp))

    f = open("output/pic33.txt","a+")
    print(out_data,file=f)
    f.close()

def run_pic(scenario):
    pic1(scenario)
    pic3_1(scenario)
    pic3(scenario)
    pic4(scenario)
    pic5(scenario)
    pic7(scenario)
    pic8(scenario)
    pic9(scenario)
    pic10(scenario)
    pic11(scenario)
    pic12(scenario)
    pic13(scenario)
    pic14(scenario)
    pic15(scenario)
    pic16(scenario)
    pic17(scenario)
    pic18(scenario)
    pic19(scenario)
    pic20(scenario)
    pic21(scenario)
    pic23(scenario)
    pic24(scenario)
    pic26(scenario)
    pic28(scenario)
    pic29(scenario)
    pic30(scenario)
    pic31(scenario)
    pic32(scenario)
    pic33(scenario)


def main():
    global db_con,cursor

    db_con = pymysql.connect(host="db", port=3306, user="root", password='12345',
                         database="log_aggregation")
    cursor = db_con.cursor()
    
    run_pic("ai")
    run_pic("serverless")
    run_pic("component")
    run_pic("video")
    run_pic("edge")

if __name__ == '__main__':
    main()
