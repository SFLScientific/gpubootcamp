# k8s single user version docker image

The image contains the workshop with all requirements and datasets pre-installed/downloaded.
It is able to be ran on its own with `docker run --rm -it -p 8888:8888 image_name` to run the workshop as normal.
It is also able to be ran in a jupyterhub k8s setup.

To build the image, run `build.sh` or `docker build -t image_name -f k8s-docker/Dockerfile .` from the root of the repo.