#!/usr/bin/env python

# ---------------------------------------------------------
# IOU Tracker
# Copyright (c) 2017 TU Berlin, Communication Systems Group
# Licensed under The MIT License [see LICENSE for details]
# Written by Erik Bochinski
# ---------------------------------------------------------

from time import time
import argparse

from iou_tracker import track_iou
from util import load_mot, save_to_csv


def main(args):
    with open(args.seqmap) as fd:
        seqs = [line.rstrip('\n') for line in fd]

    for idx, seq in enumerate(seqs):
        if seq == "name" or seq == "":
            continue
        else:
            det_path = args.benchmark_dir + "/" + seq + "/det/det.txt"
            out_path = args.res_dir + "/" + seq + ".txt"

            detections = load_mot(det_path, with_classes=False)

            start = time()
            tracks = track_iou(detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)
            end = time()

            num_frames = len(detections)
            print("finished " + seq + " at " + str(int(num_frames / (end - start))) + " fps!")

            save_to_csv(out_path, tracks)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="IOU Tracker MOT demo script. Default parameters are set to reproduce "
                                                 "the results using the SDP detections.")
    parser.add_argument('-m', '--seqmap', type=str, required=True,
                        help="full path to the seqmap file to evaluate")
    parser.add_argument('-o', '--res_dir', type=str, required=True,
                        help="path to the results directory")
    parser.add_argument('-b', '--benchmark_dir', type=str, required=True,
                        help="path to the sequence directory")
    parser.add_argument('-sl', '--sigma_l', type=float, default=0.3,
                        help="low detection threshold")
    parser.add_argument('-sh', '--sigma_h', type=float, default=0.5,
                        help="high detection threshold")
    parser.add_argument('-si', '--sigma_iou', type=float, default=0.3,
                        help="intersection-over-union threshold")
    parser.add_argument('-tm', '--t_min', type=float, default=5,
                        help="minimum track length")

    args = parser.parse_args()
    main(args)
