#/bin/bash

ffmpeg -r 3 -i out%d.png out.gif
