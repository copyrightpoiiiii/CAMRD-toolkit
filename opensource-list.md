# 开源代码清单

## Log trace 分析(Log_trace_analyze)

1. Log trace聚合
    
    log_aggregation.py, match_apicall.py

2. Log 指标采集

    collect_log_metrics.py

3. 镜像依赖关系分析

    dependency_repo.py, dependency_tag.py

## I/O trace 采集(I/O trace acquisition)

1. 镜像启动数据采集
   
   cntr-tracer.c, cntracer.py

2. 镜像IO延迟采集

    dog.c

## 镜像内容分析(Image content analyze)

1. 文件访问热度分析

   main.go

## 仓库去重分析(Registry duplication analyze)

1. 镜像信息采集

   database.py, docker.py, dockerhub.py

2. 镜像冗余分析

   query.py, redundancy.py, similarity.py

## 论文测试相关(Experimerntal tests)

1. 转换时间模拟测试

   image_conversion.py

2. 启动时间模拟测试

   image_startup/main.go
