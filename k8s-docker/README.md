# k8s single user version docker image

Docker image to replicate base notebook image from [here](https://github.com/jupyter/docker-stacks/tree/master/base-notebook) but based on nvidia/cuda 20.04 along with Dask and Rapids installed and functional from notebooks.

Compatible with jupyterhub (since rapids docker image isnt) and runnable standalone.

Build command `docker build -f Dockerfile -t rapidsjhubsingleruser .`

