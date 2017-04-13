#!/bin/bash

set -x

wget https://www.physionet.org/pn3/ecgiddb/RECORDS

datadir=data/

while read row; do
	echo "Downloading $row"
	dir=$(dirname $row)
	base=$(basename $row)
	mkdir -p "$data/$dir"
	exts="atr dat hea"
	pushd "$data/$dir"
	for ext in $exts; do
		filename=$base.$ext
		echo "Downlading file $filename"
		wget https://www.physionet.org/pn3/ecgiddb/Person_01/$filename
	done
	popd
done < RECORDS

rm RECORDS
