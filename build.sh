#!/bin/bash

# run from repo root
docker build -t nickssmith/gpubootcamp-k8s-data -f k8s-docker/Dockerfile .

# run from k8s-docker
# docker build -t nickssmith/gpubootcamp-k8s-data -f Dockerfile ../.