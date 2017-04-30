#!/bin/bash

set -x

mkdir -p "data/mitdb"
cd "data/mitdb"

exts="atr dat hea"
for ext in $exts; do
	for rec in {100..124}; do
		filename=$rec.$ext
		wget https://physionet.org/physiobank/database/mitdb/$filename
	done
	for rec in {200..234}; do
		filename=$rec.$ext
		wget https://physionet.org/physiobank/database/mitdb/$filename
	done
done
