FROM osrf/ros:humble-desktop

ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=eagle
ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake gdb git clang-format \
        can-utils iproute2 kmod \
        python3-pip python3-colcon-common-extensions \
        ros-humble-ros2-socketcan \
        ros-humble-plotjuggler-ros \
        ros-humble-tf2-tools \
        ros-humble-tf-transformations \
        ros-humble-rqt-graph \
        sudo \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir "python-can>=4.3" cantools

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && echo "source /opt/ros/humble/setup.bash" >> /home/${USERNAME}/.bashrc

USER ${USERNAME}
WORKDIR /home/${USERNAME}/ws
CMD ["bash"]
