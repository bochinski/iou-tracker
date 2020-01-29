# ---------------------------------------------------------
# IOU Tracker
# Copyright (c) 2019 TU Berlin, Communication Systems Group
# Licensed under The MIT License [see LICENSE for details]
# Written by Erik Bochinski
# ---------------------------------------------------------

import cv2

KCF2_available = True
try:
    import KCF
except ImportError:
    KCF = None
    KCF2_available = False


class VisTracker:
    kcf2_warning_printed = False

    def __init__(self, tracker_type, bbox, img, keep_height_ratio=1.):
        """ Wrapper class for various visual trackers."
        Args:
            tracker_type (str): name of the tracker. either the ones provided by opencv-contrib or KCF2 for a different
                                implementation for KCF (requires https://github.com/uoip/KCFcpp-py-wrapper)
            bbox (tuple): box to initialize the tracker (x1, y1, x2, y2)
            img (numpy.ndarray): image to intialize the tracker
            keep_height_ratio (float, optional): float between 0.0 and 1.0 that determines the ratio of height of the
                                                 object to track to the total height of the object for visual tracking.
        """
        if tracker_type == 'KCF2' and not KCF:
            tracker_type = 'KCF'
            if not VisTracker.kcf2_warning_printed:
                print("[warning] KCF2 not available, falling back to KCF. please see README.md for further details")
                VisTracker.kcf2_warning_printed = True

        self.tracker_type = tracker_type
        self.keep_height_ratio = keep_height_ratio

        if tracker_type == 'BOOSTING':
            self.vis_tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            self.vis_tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            self.vis_tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'KCF2':
            self.vis_tracker = KCF.kcftracker(False, True, False, False)  # hog, fixed_window, multiscale, lab
        elif tracker_type == 'TLD':
            self.vis_tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            self.vis_tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
            self.vis_tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'NONE':  # dummy tracker that does nothing but fail
            self.vis_tracker = None
            self.ok = False
            return
        else:
            raise ValueError("Unknown tracker type '{}".format(tracker_type))

        y_max = img.shape[0] - 1
        x_max = img.shape[1] - 1
        #
        bbox = list(bbox)
        bbox[0] = max(0, min(bbox[0], x_max))
        bbox[2] = max(0, min(bbox[2], x_max))
        bbox[1] = max(0, min(bbox[1], y_max))
        bbox[3] = max(0, min(bbox[3], y_max))

        bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]  # x1, y1, x2, y2 -> x1, y1, w, h
        bbox[3] *= self.keep_height_ratio

        if self.tracker_type == 'KCF2':
            self.vis_tracker.init(bbox, img)
            self.ok = True
        else:
            self.ok = self.vis_tracker.init(img, tuple(bbox))
            pass

    def update(self, img):
        """
        Args:
            img (numpy.ndarray): image for update

        Returns:
        bool: True if the update was successful, False otherwise
        tuple: updated bounding box in (x1, y1, x2, y2) format
        """
        if not self.ok:
            return False, [0, 0, 0, 0]

        if self.tracker_type == 'KCF2':
            bbox = self.vis_tracker.update(img)
            ok = True
        else:
            ok, bbox = self.vis_tracker.update(img)
            bbox = list(bbox)

        bbox[3] /= self.keep_height_ratio
        # x1, y1, w, h -> x1, y1, x2, y2
        bbox[2] += bbox[0]
        bbox[3] += bbox[1]

        return ok, tuple(bbox)
