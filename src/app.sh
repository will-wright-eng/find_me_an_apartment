#!/bin/bash

rm -r __pycache__
mkdir csvs
mkdir images

start=`date +%s`

python main.py

end=`date +%s`
runtime=$((end-start))
echo process runtime in seconds
echo $runtime