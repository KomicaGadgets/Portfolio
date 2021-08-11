FROM ubuntu:20.10
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /rlang

RUN sed -i 's/archive.ubuntu.com/free.nchc.org.tw/g' /etc/apt/sources.list

RUN apt-get update -qq && \
	apt-get install -y wget ca-certificates zip unzip python3-dev python3-pip r-base

RUN R -e 'install.packages("randomForest")'

RUN python3 -m pip install rpy2 && \
	rm -rf $HOME/.cache/pip

RUN apt-get autoremove -y && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
