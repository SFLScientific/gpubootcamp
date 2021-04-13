FROM nvcr.io/nvidia/tensorflow:20.01-tf2-py3
LABEL maintainer="Nick Smith <nsmith@sflscientific.com>"


# Set user ID and name
ARG NB_USER="workshopuser"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -q update \
 && apt-get install -yq --no-install-recommends \
    wget \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    run-one \
    libsm6 libxext6 libxrender-dev git nvidia-modprobe\
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen


# Configure environment
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV HOME=/home/$NB_USER



# Copy a script that we will use to correct permissions after running certain commands
COPY k8s-docker/fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc 

# Create NB_USER with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    chmod g+w /etc/passwd && \
    fix-permissions $HOME

# fix the permissions of the home directory
USER $NB_UID
RUN fix-permissions "/home/$NB_USER"


USER root

# install requirements for the workshop
RUN pip install opencv-python==4.1.2.30 pandas seaborn sklearn matplotlib scikit-fmm tqdm h5py gdown

# generate the config for jhub
RUN jupyter notebook --generate-config && \
    jupyter lab clean && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions /home/$NB_USER

EXPOSE 8888

# Configure container startup
CMD ["start-notebook.sh"]

# Copy local files as late as possible to avoid cache busting
COPY k8s-docker/start.sh k8s-docker/start-notebook.sh k8s-docker/start-singleuser.sh /usr/local/bin/
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY k8s-docker/jupyter_notebook_config.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root

# Prepare upgrade to JupyterLab V3.0 #1205
RUN sed -re "s/c.NotebookApp/c.ServerApp/g" \
    /etc/jupyter/jupyter_notebook_config.py > /etc/jupyter/jupyter_server_config.py

RUN fix-permissions /etc/jupyter/


# copy the workshop files into place

# Climate notebooks
COPY hpc_ai/ai_science_climate/English/ $HOME/Climate
# Pre-Download the Dataset
RUN python3 $HOME/Climate/python/source_code/dataset.py


# CFD notebools
COPY hpc_ai/ai_science_cfd/English/ $HOME/CFD
# Pre-download the dataset
RUN mkdir -p /home/$NB_USER/CFD/python/jupyter_notebook/CFD/data
RUN python3 $HOME/CFD/python/source_code/dataset.py

# Take ownership of the home directory
RUN chown -R $NB_USER $HOME/**

# Install jhub for singe-user commands to be available
RUN pip install jupyter jupyterlab jupyterhub

# work as notebook user
USER $NB_UID
WORKDIR $HOME




