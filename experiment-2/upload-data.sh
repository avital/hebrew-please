#!/bin/bash

set -e

if [ -x ${GPU_MACHINE} ]; then
   echo 'Set $GPU_MACHINE'
   exit 1
fi

rm -f data.tar.gz
tar cfvz data.tar.gz $(find data/ -name '*.mp3')
ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} "mkdir -p hebrew-please"
scp -i "${HOME}/avital2.pem" data.tar.gz ubuntu@${GPU_MACHINE}:~/hebrew-please/data.tar.gz
ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} "cd hebrew-please && rm -rf data && tar xfvz data.tar.gz"
ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} "cd hebrew-please/data && for f in \$(find . -name '*.mp3'); do echo \$f; done"
ssh -i "${HOME}/avital2.pem" ubuntu@${GPU_MACHINE} "cd hebrew-please/data && for f in \$(find . -name '*.mp3'); do ffmpeg -i \$f -ar 22050 -ac 1 \$(echo \$f | sed 's/\.mp3/.wav/'); done"

