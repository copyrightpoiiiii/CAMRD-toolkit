> This project consists of the dataset, tools, and analysis scripts covered in our paper ***A Comprehensive Analysis of Container Image Traces from Real-world Scenarios***.
>># Dataset
>>In our paper, we collected a large number of traces from five real-world scenarios (Serverless / AI / Edge / Video analytic / Component) for data analysis and downloaded top100 images from Docker Hub for a performance comparison. Since traces from real-world scenarios are being processed, desensitized and authorized by the trace provider, they cannot be disclosed on the Github at the moment. But we promise that the trace will be open-sourced in a few months. At this time, we can only describe some samples shown in [*Log trace*](DataSet/Log_trace_sample). 
>>And for performance comparison, all traces are available in [*I/O trace*](DataSet/IO_trace).
>> - Dataset
>>   - log trace:   
>>        [Serverless_sample](DataSet/Log_trace_sample/serverless_sample.json)
>>
>>        [AI_sample](DataSet/Log_trace_sample/ai_sample.json)
>>
>>        [Edge_sample](DataSet/Log_trace_sample/edge_sample.json)
>>
>>        [Video_sample](DataSet/Log_trace_sample/video_sample.json)
>>
>>        [Component_sample](DataSet/Log_trace_sample/component_sample.json)
>>   - I/O trace:  
>>        [i/o traces of top100 images](DataSet/IO_trace/Accessed_file.csv)
>>
>>        [i/o latency](DataSet/IO_trace/IO_latency.csv)
>># Tools
>>In our paper, there are three tools. One is the log trace analysis tool, presented in [*Log trace analyze*](Tools/Log_trace_analyze); one is the registry duplication analysis tool, shown in [*registry duplication analyze*](Tools/Deduplication). And the I/O trace analysis tool, for the copyright reason, is also not open-sourced at this time. When the authorization is available, it will be released. 
>>- Tools
>>   - log trace analyze
>>   - registry duplication analyze
>># Analysis scripts
>>All analysis scripts in our experiments are uploaded in [*Experimental tests*](Experimental_tests).
>>- Experimental tests
>>   - [log: statistic](Experimental_tests/Log_metrics_collected/collect_log_metrics.py)
>>   - [conversion](Experimental_tests/Image_conversion/image_conversion.py)
>>   - [comparison](Experimental_tests/Image_startup/main.go)