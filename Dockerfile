FROM nvidia/cuda:7.5-cudnn5-devel-ubuntu14.04
MAINTAINER caffe-maint@googlegroups.com

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        libgeos-dev \
        protobuf-compiler \
        python-dev \
        python-pip \
        python-scipy \
        python-skimage \
        python-opencv && \
    rm -rf /var/lib/apt/lists/*

ENV CAFFE_ROOT=/opt/caffe
WORKDIR $CAFFE_ROOT

# FIXME: clone a specific git tag and use ARG instead of ENV once DockerHub supports this.
ENV CLONE_TAG=experimental

# Clone Repo
RUN git clone -b ${CLONE_TAG} --depth 1 "https://github.com/aaide/TextBoxes_plusplus.git" .

# Update pip before installing stuff (apt-get pip is quite old)
RUN sudo pip install -U pip

# Resolve version conflict with six
RUN pip install --ignore-installed six

# Install GCC5 to make caffe building work
RUN sudo apt-get -Y update && \
	sudo apt-get -Y install software-properties-common && \
	sudo add-apt-repository ppa:ubuntu-toolchain-r/test && \
	sudo apt-get -Y install gcc-5 g++-5 && \
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5

# Install requirements and build caffe
RUN for req in $(cat python/requirements.txt); do pip install $req; done && \
    mkdir build && cd build && \
    cmake .. -DCUDA_ARCH_NAME=Manual && \
    make -j"$(nproc)"

# HACK: OpenCV can be confused by (the lack of) this driver in some systems
RUN ln /dev/null /dev/raw1394

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

WORKDIR /opt/caffe
