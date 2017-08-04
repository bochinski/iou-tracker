# ---------------------------------------------------------
# IOU Tracker
# Copyright (c) 2017 TU Berlin, Communication Systems Group
# Licensed under The MIT License [see LICENSE for details]
# Written by Erik Bochinski
# ---------------------------------------------------------

import numpy as np
import csv


def load_mot(detections):
    """
    Loads detections stored in a mot-challenge like formatted CSV or numpy array (fieldNames = ['frame', 'id', 'x', 'y',
    'w', 'h', 'score']).

    Args:
        detections

    Returns:
        list: list containing the detections for each frame.
    """

    data = []
    if type(detections) is str:
        raw = np.genfromtxt(detections, delimiter=',', dtype=np.float32)
    else:
        # assume it is an array
        assert isinstance(detections, np.ndarray), "only numpy arrays or *.csv paths are supported as detections."
        raw = detections.astype(np.float32)

    end_frame = int(np.max(raw[:, 0]))
    for i in range(1, end_frame+1):
        idx = raw[:, 0] == i
        bbox = raw[idx, 2:6]
        bbox[:, 2:4] += bbox[:, 0:2]  # x1, y1, w, h -> x1, y1, x2, y2
        scores = raw[idx, 6]
        dets = []
        for bb, s in zip(bbox, scores):
            dets.append({'bbox': (bb[0], bb[1], bb[2], bb[3]), 'score': s})
        data.append(dets)

    return data


def save_to_csv(out_path, tracks):
    """
    Saves tracks to a CSV file.

    Args:
        out_path (str): path to output csv file.
        tracks (list): list of tracks to store.
    """

    with open(out_path, "w") as ofile:
        field_names = ['frame', 'id', 'x', 'y', 'w', 'h', 'score', 'wx', 'wy', 'wz']

        odict = csv.DictWriter(ofile, field_names)
        id_ = 1
        for track in tracks:
            for i, bbox in enumerate(track['bboxes']):
                row = {'id': id_,
                       'frame': track['start_frame'] + i,
                       'x': bbox[0],
                       'y': bbox[1],
                       'w': bbox[2] - bbox[0],
                       'h': bbox[3] - bbox[1],
                       'score': track['max_score'],
                       'wx': -1,
                       'wy': -1,
                       'wz': -1}

                odict.writerow(row)
            id_ += 1


def iou(bbox1, bbox2):
    """
    Calculates the intersection-over-union of two bounding boxes.

    Args:
        bbox1 (numpy.array, list of floats): bounding box in format x1,y1,x2,y2.
        bbox2 (numpy.array, list of floats): bounding box in format x1,y1,x2,y2.

    Returns:
        int: intersection-over-onion of bbox1, bbox2
    """

    bbox1 = [float(x) for x in bbox1]
    bbox2 = [float(x) for x in bbox2]

    (x0_1, y0_1, x1_1, y1_1) = bbox1
    (x0_2, y0_2, x1_2, y1_2) = bbox2

    # get the overlap rectangle
    overlap_x0 = max(x0_1, x0_2)
    overlap_y0 = max(y0_1, y0_2)
    overlap_x1 = min(x1_1, x1_2)
    overlap_y1 = min(y1_1, y1_2)

    # check if there is an overlap
    if overlap_x1 - overlap_x0 <= 0 or overlap_y1 - overlap_y0 <= 0:
        return 0

    # if yes, calculate the ratio of the overlap to each ROI size and the unified size
    size_1 = (x1_1 - x0_1) * (y1_1 - y0_1)
    size_2 = (x1_2 - x0_2) * (y1_2 - y0_2)
    size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0)
    size_union = size_1 + size_2 - size_intersection

    return size_intersection / size_union
