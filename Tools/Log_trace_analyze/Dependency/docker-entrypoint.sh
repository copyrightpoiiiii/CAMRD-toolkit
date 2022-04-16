#!/bin/bash
python dependency_repo.py ai_repo.out ai_repo.pair ai 12345
python dependency_tag.py 12345 ai ai_tag.out
echo ai_repo
cat ai_repo.out
echo ai_repo_pair
cat ai_repo.pair
echo ai_tag
echo ai_tag.out
python dependency_repo.py serverless_repo.out serverless_repo.pair serverless 12345
python dependency_tag.py 12345 serverless serverless_tag.out
echo serverless_repo
cat serverless_repo.out
echo serverless_repo_pair
cat serverless_repo.pair
echo serverless_tag
echo serverless_tag.out
python dependency_repo.py component_repo.out component_repo.pair component 12345
python dependency_tag.py 12345 component component_tag.out
echo component_repo
cat component_repo.out
echo component_repo_pair
cat component_repo.pair
echo component_tag
echo component_tag.out
python dependency_repo.py video_repo.out video_repo.pair video 12345
python dependency_tag.py 12345 video video_tag.out
echo video_repo
cat video_repo.out
echo video_repo_pair
cat video_repo.pair
echo video_tag
echo video_tag.out
python dependency_repo.py edge_repo.out edge_repo.pair edge 12345
python dependency_tag.py 12345 edge edge_tag.out
echo edge_repo
cat edge_repo.out
echo edge_repo_pair
cat edge_repo.pair
echo edge_tag
echo edge_tag.out
python collect_log_metrics.py
echo layer_size
cat output/pic4.txt
echo image_size
cat output/pic3_1.txt
echo cdf_for_layerSize_requests
cat output/pic31.txt
echo cdf_for_imageSize_requests
cat output/pic32.txt
echo cdf_for_layer_pull_time
cat output/pic11.txt
echo cdf_for_image_pull
cat output/pic5.txt
echo the_interval_for_the_same_layer_pull
cat output/pic26.txt
echo the_interval_for_the_same_image_pull
cat output/pic24.txt
echo layer_first_request_last_request
cat output/pic28.txt
echo image_pull_interval
cat output/pic8.txt
echo cdf_for_layer_pulled_by_node
cat output/pic29.txt
echo cdf_for_nodes_pull_images
cat output/pic7.txt
echo cdf_for_nodes_pull_layers
cat output/pic13.txt
echo cdf_for_images_pulled
cat output/pic10.txt
echo gap_between_upload_pull
cat output/pic17.txt
echo the_interval_for_the_same_image_request
cat output/pic9.txt
echo cdf_for_node_pull_image
cat output/pic18.txt
echo gap_between_upload_pull_for_node
cat output/pic19.txt
echo cdf_for_nodes_pull_repo
cat output/pic30.txt
echo cdf_for_repo_request
cat output/pic21.txt
echo cdf_for_repo_nodes
cat output/pic23.txt
echo layer_in_images_cdf
cat output/pic15.txt
echo layer_in_repos_cdf
cat output/pic16.txt
