# Dockerfile for running tensorflow with ipykernel by starting a jupyter notebook

# To build the docker container, run: $ sudo docker build -t ai-science-cfd:latest --network=host .
# To run: $ sudo docker run --rm -it --gpus=all -p 8888:8888 ai-science-cfd:latest
# Finally, open http://127.0.0.1:8888/

# Select Base Image 
FROM nvcr.io/nvidia/tensorflow:20.01-tf2-py3
# Update the repo
RUN apt-get update
# Install required dependencies
RUN apt-get install -y libsm6 libxext6 libxrender-dev git
# Copy required python packages
COPY requirements.py3.txt /tmp/requirements.py3.txt
# Install required packages
RUN pip3 install -r /tmp/requirements.py3.txt
# Copy the IPY Kernel
COPY ipykernel-k8s.py .
# Copy the working hpc_ai directory
COPY /hpc_ai .
# TO COPY the data
COPY /hpc_ai/ai_science_cfd/English/ /workspace/
# Make a directory for Data
RUN mkdir /workspace/python/jupyter_notebook/CFD/data
# Run the Python
RUN python3 /workspace/python/source_code/dataset.py
## Connect the Jupyter Notebook
CMD jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=8888 --NotebookApp.token="" --notebook-dir=/workspace/python/jupyter_notebook/
