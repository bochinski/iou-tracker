#!/bin/bash

# set these variables according to your setup
seq_dir=/path/to/cvpr19/train # base directory of the split (cvpr19/train, cvpr19/test etc.)
results_dir=results/cvpr19    # output directory, will be created if not existing


mkdir -p ${results_dir}

options="-v KCF2 -sl 0.3 -sh 0.8 -si 0.4 -tm 5 --ttl 20 -hr 0.3 -fmt motchallenge"
for seq in $(ls $seq_dir); do
  echo $seq
  python demo.py -f ${seq_dir}/${seq}/img1/{:06d}.jpg -d ${seq_dir}/${seq}/det/det.txt \
  -o ${results_dir}/${seq}.txt ${options}
done
