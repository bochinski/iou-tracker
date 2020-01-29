#!/usr/bin/env python

# ---------------------------------------------------------
# IOU Tracker
# Copyright (c) 2017 TU Berlin, Communication Systems Group
# Licensed under The MIT License [see LICENSE for details]
# Written by Erik Bochinski
# ---------------------------------------------------------

import argparse

from iou_tracker import track_iou
from viou_tracker import track_viou
from util import load_mot, save_to_csv


def main(args):
    formats = ['motchallenge', 'visdrone']
    assert args.format in formats, "format '{}' unknown supported formats are: {}".format(args.format, formats)

    with_classes = False
    if args.format == 'visdrone':
        with_classes = True
    detections = load_mot(args.detection_path, nms_overlap_thresh=args.nms, with_classes=with_classes)

    if args.visual:
        tracks = track_viou(args.frames_path, detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min,
                            args.ttl, args.visual, args.keep_upper_height_ratio)
    else:
        if with_classes:
            # track_viou can also be used without visual tracking, but note that the speed will be much slower compared
            # to track_iou. However, this way supports the optimal LAP solving and the handling of multiple object classes:
            tracks = track_viou(args.frames_path, detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min,
                                args.ttl, 'NONE', args.keep_upper_height_ratio)
        else:
            tracks = track_iou(detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)

    save_to_csv(args.output_path, tracks, fmt=args.format)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="IOU/V-IOU Tracker demo script")
    parser.add_argument('-v', '--visual', type=str, help="visual tracker for V-IOU. Currently supported are "
                                                         "[BOOSTING, MIL, KCF, KCF2, TLD, MEDIANFLOW, GOTURN, NONE] "
                                                         "see README.md for furthert details")
    parser.add_argument('-hr', '--keep_upper_height_ratio', type=float, default=1.0,
                        help="Ratio of height of the object to track to the total height of the object "
                             "for visual tracking. e.g. upper 30%%")
    parser.add_argument('-f', '--frames_path', type=str,
                        help="sequence frames with format '/path/to/frames/frame_{:04d}.jpg' where '{:04d}' will "
                             "be replaced with the frame id. (zero_padded to 4 digits, use {:05d} for 5 etc.)")
    parser.add_argument('-d', '--detection_path', type=str, required=True,
                        help="full path to CSV file containing the detections")
    parser.add_argument('-o', '--output_path', type=str, required=True,
                        help="output path to store the tracking results "
                             "(MOT challenge/Visdrone devkit compatible format)")
    parser.add_argument('-sl', '--sigma_l', type=float, default=0,
                        help="low detection threshold")
    parser.add_argument('-sh', '--sigma_h', type=float, default=0.5,
                        help="high detection threshold")
    parser.add_argument('-si', '--sigma_iou', type=float, default=0.5,
                        help="intersection-over-union threshold")
    parser.add_argument('-tm', '--t_min', type=float, default=2,
                        help="minimum track length")
    parser.add_argument('-ttl', '--ttl', type=int, default=1,
                        help="time to live parameter for v-iou")
    parser.add_argument('-nms', '--nms', type=float, default=None,
                        help="nms for loading multi-class detections")
    parser.add_argument('-fmt', '--format', type=str, default='motchallenge',
                        help='format of the detections [motchallenge, visdrone]')

    args = parser.parse_args()
    assert not args.visual or args.visual and args.frames_path, "visual tracking requires video frames, " \
                                                                "please specify via --frames_path"

    assert 0.0 < args.keep_upper_height_ratio <= 1.0, "only values between 0 and 1 are allowed"
    assert args.nms is None or 0.0 <= args.nms <= 1.0, "only values between 0 and 1 are allowed"
    main(args)
