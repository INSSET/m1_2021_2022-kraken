#!/bin/bash

service ssh start
/usr/sbin/sshd -D&

cd /home/gestproj/api && python3 -m flask run --host=0.0.0.0

