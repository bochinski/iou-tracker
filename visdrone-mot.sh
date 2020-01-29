#!/bin/bash

# set these variables according to your setup
visdrone_dir=/path/to/VisDrone2018-MOT-val  # base directory of the split (VisDrone2018-MOT-val, VisDrone2018-MOT-train etc.)
results_dir=results/VisDrone2018-MOT-val    # output directory, will be created if not existing
vis_tracker=MEDIANFLOW                      # [MEDIANFLOW, KCF2, NONE] parameter set as used in the paper


if [ "${vis_tracker}" = "MEDIANFLOW" ]; then
  options="-v MEDIANFLOW  -sl 0.9 -sh 0.98 -si 0.1 -tm 23 --ttl 8 --nms 0.6 -fmt visdrone"
elif [ "${vis_tracker}" = "KCF2" ]; then
  options="-v KCF2 -sl 0.9 -sh 0.98 -si 0.05 -tm 23 --ttl 8 --nms 0.6 -fmt visdrone"
elif [ "${vis_tracker}" = "NONE" ]; then
  options="-sl 0.5 -sh 0.98 -si 0.05 -tm 7 --nms 0.6 -fmt visdrone"
else
  echo "unknown tracker '${vis_tracker}'"
  exit
fi

mkdir -p ${results_dir}

seq_dir=${visdrone_dir}/sequences

echo "using '${vis_tracker}' option for visual tracking:"
echo "${options}"
for seq in $(ls $seq_dir); do
  echo "processing ${seq} ...."

  python demo.py -f ${seq_dir}/${seq}/{:07d}.jpg -d ${visdrone_dir}/detections/${seq}.txt \
         -o ${results_dir}/${seq}.txt ${options}
done
