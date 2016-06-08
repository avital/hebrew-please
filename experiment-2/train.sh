#!/bin/bash

if [ -x ${GPU_MACHINE} ]; then
   echo 'Set $GPU_MACHINE'
   exit 1
fi

scp -i "${HOME}/avital2.pem" train.py ubuntu@${GPU_MACHINE}:~/hebrew-please/train.py

# Set up /dev/nvidia0
#ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} 'sudo mknod -m 666 /dev/nvidia0 c 195 0 && sudo mknod -m 666 /dev/nvidia-uvm c 251 0 && sudo mknod -m 666 /dev/nvidiactl c 195 255'

# Install Docker if not already installed
#ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} 'docker -v || curl -fsSL https://get.docker.com/# | sh'

#ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} 'cd hebrew-please && sudo nvidia-docker run -v ${PWD}:/root/hebrew-please avital/keras bash -c "cd ../hebrew-please && THEANO_FLAGS=device=gpu,floatX=float32 python train.py"'

ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} 'cd hebrew-please && nohup bash -c "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64 KERAS_BACKEND=tensorflow python train.py"'

