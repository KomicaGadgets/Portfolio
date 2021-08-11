FROM ubuntu:19.10

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /var/www

RUN apt-get -y update \
    && apt-get -y install \
	zip unzip python3-dev python3-pip \
	cmake libopenmpi-dev python3-dev zlib1g-dev \
	libsm6 libxext6 libxrender-dev libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && \
    pip3 install Cython gym stable-baselines[mpi] arrow \
	opencv-python pyppeteer
RUN python3 -m pip install --upgrade https://github.com/evdcush/TensorFlow-wheels/releases/download/tf-1.13.1-py37-cpu-ivybridge/tensorflow-1.13.1-cp37-cp37m-linux_x86_64.whl && \
	pip3 install tensorflow==1.14.0 && \
    rm -rf $HOME/.cache/pip

CMD ["/bin/bash"]
