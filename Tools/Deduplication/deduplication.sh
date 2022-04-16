#!/bin/bash
docker pull julia:buster
docker pull julia:bullseye
docker pull adminer:standalone
docker pull adminer:fastcgi
docker pull kong:latest
docker pull kong:ubuntu
docker pull crux:3.4
docker pull crux:3.2
docker pull joomla:php8.1-fpm-alpine
docker pull joomla:php8.1-fpm
python Deduplication/main.py --use-db --load-info
echo "Redundancy of file level"
cat Deduplication/DataSet/Redundancy_file_level.csv