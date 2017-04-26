#/bin/bash

ffmpeg -r 6 -i out%d.png out.avi

for id in {2..100000}; do
	if [ -f diff$((id-1)).png ]; then
		echo diff$((id-1)).png cached
		continue
	fi
	if [ ! -f out$id.png ]; then
		echo out$id.png dont exists
		break
	fi
	compare out$id.png out$((id-1)).png -compose src diff$((id-1)).png
done

ffmpeg -r 6 -i diff%d.png diff.avi
