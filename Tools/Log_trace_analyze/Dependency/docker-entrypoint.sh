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
python print_pics.py

