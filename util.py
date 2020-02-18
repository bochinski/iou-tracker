# ---------------------------------------------------------
# IOU Tracker
# Copyright (c) 2017 TU Berlin, Communication Systems Group
# Licensed under The MIT License [see LICENSE for details]
# Written by Erik Bochinski
# ---------------------------------------------------------

import numpy as np
import csv
import os


visdrone_classes = {'car': 4, 'bus': 9, 'truck': 6, 'pedestrian': 1, 'van': 5}


def load_mot(detections, nms_overlap_thresh=None, with_classes=True, nms_per_class=False):
    """
    Loads detections stored in a mot-challenge like formatted CSV or numpy array (fieldNames = ['frame', 'id', 'x', 'y',
    'w', 'h', 'score']).

    Args:
        detections (str, numpy.ndarray): path to csv file containing the detections or numpy array containing them.
        nms_overlap_thresh (float, optional): perform non-maximum suppression on the input detections with this thrshold.
                                              no nms is performed if this parameter is not specified.
        with_classes (bool, optional): indicates if the detections have classes or not. set to false for motchallange.
        nms_per_class (bool, optional): perform non-maximum suppression for each class separately

    Returns:
        list: list containing the detections for each frame.
    """
    if nms_overlap_thresh:
        assert with_classes, "currently only works with classes available"

    data = []
    if type(detections) is str:
        raw = np.genfromtxt(detections, delimiter=',', dtype=np.float32)
        if np.isnan(raw).all():
            raw = np.genfromtxt(detections, delimiter=' ', dtype=np.float32)

    else:
        # assume it is an array
        assert isinstance(detections, np.ndarray), "only numpy arrays or *.csv paths are supported as detections."
        raw = detections.astype(np.float32)

    end_frame = int(np.max(raw[:, 0]))
    for i in range(1, end_frame+1):
        idx = raw[:, 0] == i
        bbox = raw[idx, 2:6]
        bbox[:, 2:4] += bbox[:, 0:2]  # x1, y1, w, h -> x1, y1, x2, y2
        bbox -= 1  # correct 1,1 matlab offset
        scores = raw[idx, 6]

        if with_classes:
            classes = raw[idx, 7]

            bbox_filtered = None
            scores_filtered = None
            classes_filtered = None
            for coi in visdrone_classes:
                cids = classes==visdrone_classes[coi]
                if nms_per_class and nms_overlap_thresh:
                    bbox_tmp, scores_tmp = nms(bbox[cids], scores[cids], nms_overlap_thresh)
                else:
                    bbox_tmp, scores_tmp = bbox[cids], scores[cids]

                if bbox_filtered is None:
                    bbox_filtered = bbox_tmp
                    scores_filtered = scores_tmp
                    classes_filtered = [coi]*bbox_filtered.shape[0]
                elif len(bbox_tmp) > 0:
                    bbox_filtered = np.vstack((bbox_filtered, bbox_tmp))
                    scores_filtered = np.hstack((scores_filtered, scores_tmp))
                    classes_filtered += [coi] * bbox_tmp.shape[0]

            if bbox_filtered is not None:
                bbox = bbox_filtered
                scores = scores_filtered
                classes = classes_filtered

            if nms_per_class is False and nms_overlap_thresh:
                bbox, scores, classes = nms(bbox, scores, nms_overlap_thresh, np.array(classes))

        else:
            classes = ['pedestrian']*bbox.shape[0]

        dets = []
        for bb, s, c in zip(bbox, scores, classes):
            dets.append({'bbox': (bb[0], bb[1], bb[2], bb[3]), 'score': s, 'class': c})
        data.append(dets)

    return data


def nms(boxes, scores, overlapThresh, classes=None):
    """
    perform non-maximum suppression. based on Malisiewicz et al.
    Args:
        boxes (numpy.ndarray): boxes to process
        scores (numpy.ndarray): corresponding scores for each box
        overlapThresh (float): overlap threshold for boxes to merge
        classes (numpy.ndarray, optional): class ids for each box.

    Returns:
        (tuple): tuple containing:

        boxes (list): nms boxes
        scores (list): nms scores
        classes (list, optional): nms classes if specified
    """
    # # if there are no boxes, return an empty list
    # if len(boxes) == 0:
    #     return [], [], [] if classes else [], []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    if scores.dtype.kind == "i":
        scores = scores.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    #score = boxes[:, 4]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(scores)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    if classes is not None:
        return boxes[pick], scores[pick], classes[pick]
    else:
        return boxes[pick], scores[pick]


def save_to_csv(out_path, tracks, fmt='motchallenge'):
    """
    Saves tracks to a CSV file.

    Args:
        out_path (str): path to output csv file.
        tracks (list): list of tracks to store.
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as ofile:
        if fmt == 'motchallenge':
            field_names = ['frame', 'id', 'x', 'y', 'w', 'h', 'score', 'wx', 'wy', 'wz']
        elif fmt == 'visdrone':
            field_names = ['frame', 'id', 'x', 'y', 'w', 'h', 'score', 'object_category', 'truncation', 'occlusion']
        else:
            raise ValueError("unknown format type '{}'".format(fmt))

        odict = csv.DictWriter(ofile, field_names)
        id_ = 1
        for track in tracks:
            for i, bbox in enumerate(track['bboxes']):
                row = {'id': id_,
                       'frame': track['start_frame'] + i,
                       'x': bbox[0]+1,
                       'y': bbox[1]+1,
                       'w': bbox[2] - bbox[0],
                       'h': bbox[3] - bbox[1],
                       'score': track['max_score']}
                if fmt == 'motchallenge':
                    row['wx'] = -1
                    row['wy'] = -1
                    row['wz'] = -1
                elif fmt == 'visdrone':
                    row['object_category'] = visdrone_classes[track['class']]
                    row['truncation'] = -1
                    row['occlusion'] = -1
                else:
                    raise ValueError("unknown format type '{}'".format(fmt))

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
