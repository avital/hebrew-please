#!/bin/bash

if [ -x ${GPU_MACHINE} ]; then
   echo 'Set $GPU_MACHINE'
   exit 1
fi

ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} 'sudo add-apt-repository ppa:xorg-edgers/ppa -y && sudo apt-get update && sudo apt-get install nvidia-current -y && sudo reboot now'

