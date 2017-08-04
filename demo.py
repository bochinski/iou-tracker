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
    detections = load_mot(args.detection_path)

    start = time()
    tracks = track_iou(detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)
    end = time()

    num_frames = len(detections)
    print("finished at " + str(int(num_frames / (end - start))) + " fps!")

    save_to_csv(args.output_path, tracks)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="IOU Tracker demo script")
    parser.add_argument('-d', '--detection_path', type=str, required=True,
                        help="full path to CSV file containing the detections")
    parser.add_argument('-o', '--output_path', type=str, required=True,
                        help="output path to store the tracking results (MOT challenge devkit compatible format)")
    parser.add_argument('-sl', '--sigma_l', type=float, default=0,
                        help="low detection threshold")
    parser.add_argument('-sh', '--sigma_h', type=float, default=0.5,
                        help="high detection threshold")
    parser.add_argument('-si', '--sigma_iou', type=float, default=0.5,
                        help="intersection-over-union threshold")
    parser.add_argument('-tm', '--t_min', type=float, default=2,
                        help="minimum track length")

    args = parser.parse_args()
    main(args)
