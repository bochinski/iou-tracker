## IOU Tracker
Python implementation of the IOU Tracker described in the AVSS 2017 paper
[High-Speed Tracking-by-Detection Without Using Image Information](http://elvera.nue.tu-berlin.de/files/1517Bochinski2017.pdf).

This project is released under the MIT License (details in LICENSE file).
If you think our work is useful in your research, please consider citing:

```
@INPROCEEDINGS{1517Bochinski2017,
	AUTHOR = {Erik Bochinski and Volker Eiselein and Thomas Sikora},
	TITLE = {High-Speed Tracking-by-Detection Without Using Image Information},
	BOOKTITLE = {International Workshop on Traffic and Street Surveillance for Safety and Security at IEEE AVSS 2017},
	YEAR = {2017},
	MONTH = aug,
	ADDRESS = {Lecce, Italy},
	URL = {http://elvera.nue.tu-berlin.de/files/1517Bochinski2017.pdf},
	}
```

## Demo
Several demo scripts are included to reproduce the reported results on the UA-DETRAC
and the MOT benchmark.

Basic demo script:
```
$ ./demo.py -h
usage: demo.py [-h] -d DETECTION_PATH -o OUTPUT_PATH [-sl SIGMA_L]
               [-sh SIGMA_H] [-si SIGMA_IOU] [-tm T_MIN]

IOU Tracker demo script

optional arguments:
  -h, --help            show this help message and exit
  -d DETECTION_PATH, --detection_path DETECTION_PATH
                        full path to CSV file containing the detections
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        output path to store the tracking results (MOT
                        challenge devkit compatible format)
  -sl SIGMA_L, --sigma_l SIGMA_L
                        low detection threshold
  -sh SIGMA_H, --sigma_h SIGMA_H
                        high detection threshold
  -si SIGMA_IOU, --sigma_iou SIGMA_IOU
                        intersection-over-union threshold
  -tm T_MIN, --t_min T_MIN
                        minimum track length
```

Example:
```
./demo.py -d ../mot17/train/MOT17-04-SDP/det/det.txt -o res/iou-tracker/MOT17-04-SDP.txt
```

### DETRAC
To reproduce the reported results, download and extract the [DETRAC-toolkit](http://detrac-db.rit.albany.edu/download)
and the detections you want to evaluate. Download links for the EB detections are provided below.
Clone this repository into "DETRAC-MOT-toolkit/trackers/".
Follow the instructions to configure the toolkit for tracking evaluation and set the tracker name in "DETRAC_experiment.m":

```
tracker.trackerName = 'iou-tracker';
```

and run the script.

Note that you still need a working python environment.
You should obtain something like the following results for the 'DETRAC-Train' set:

##### DETRAC-Train Results
| Detector | Rcll | Prcn | FAR | MT    | PT  | ML     | FP      | FN      | IDs   | FM    | MOTA | MOTP | MOTAL |
| -------- | ---- | ---- | --- | ----- | --- | ------ | ------- | ------- | ----- | ----- |----- |------|-------|
| EB       |22.12 |31.53 |0.26 |17.65  |13.22|18.41   |14796.52 |171806.84|2311.25|2445.89|19.41 |28.89 |19.78  |
| R-CNN    |27.86 |52.90 |0.11 |19.53  |17.03|18.56   |9047.95  |157521.18|4842.18|4969.57|25.46 |44.39 |26.29  |

##### DETRAC-Test (Overall) Results
| Detector | Rcll | Prcn | FAR | MT    | PT  | ML     | FP      | FN      | IDs   | FM    | MOTA | MOTP | MOTAL |
| -------- | ---- | ---- | --- | ----- | --- | ------ | ------- | ------- | ----- | ----- |----- |------|-------|
| EB       |22.11 |31.53 |0.26 |17.65  |13.22|18.41   |14796.52 |171806.84|2311.25|2445.89|19.41 |28.89 |19.77  |
| R-CNN    |20.37 |44.86 |0.40 |13.81  |16.40|20.69   |22535.15 |193041.87|5029.42|5795.73|16.01 |38.35 |16.81  |

##### EB detections
The public detections of [EB](http://zyb.im/research/EB/) are not available on the
DETRAC training set and miss some low scoring detections. The EB detections we used for the tables above and our
publication are available here:

* [EB Train](https://tubcloud.tu-berlin.de/s/EtC6cFEYsAU0gFQ/download)
* [EB Test](https://tubcloud.tu-berlin.de/s/oKM3dYhJbMFl1dY/download)

### MOT
To reproduce the reported MOT16 results, use the mot16.py script:

```
$ ./mot16.py -h
usage: mot16.py [-h] -m SEQMAP -o RES_DIR -b BENCHMARK_DIR [-sl SIGMA_L]
                [-sh SIGMA_H] [-si SIGMA_IOU] [-tm T_MIN]

IOU Tracker MOT demo script. Default parameters are set to reproduce the
results using the SDP detections.

optional arguments:
  -h, --help            show this help message and exit
  -m SEQMAP, --seqmap SEQMAP
                        full path to the seqmap file to evaluate
  -o RES_DIR, --res_dir RES_DIR
                        path to the results directory
  -b BENCHMARK_DIR, --benchmark_dir BENCHMARK_DIR
                        path to the sequence directory
  -sl SIGMA_L, --sigma_l SIGMA_L
                        low detection threshold
  -sh SIGMA_H, --sigma_h SIGMA_H
                        high detection threshold
  -si SIGMA_IOU, --sigma_iou SIGMA_IOU
                        intersection-over-union threshold
  -tm T_MIN, --t_min T_MIN
                        minimum track length
```

Example:
```
# SDP:
./mot16.py -m ../motchallenge/seqmaps/sdp-train.txt -o ../motchallenge/res/MOT16/iou-tracker -b ../data/mot17/train

# FRCNN:
./mot16.py -m ../motchallenge/seqmaps/frcnn-train.txt -o ../motchallenge/res/MOT16/iou-tracker -b ../data/mot17/train -sl 0 -sh 0.9 -si 0.3 -tm 5
```

You should obtain something like the following results for the train set:

##### MOT16 Train Results
| Detector | IDF1 | IDP | IDR | Rcll | Prcn | FAR | GT  | MT  | PT  | ML  | FP  | FN  | IDs | FM  | MOTA | MOTP | MOTAL |
| -------- | ---- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ----- |
|SDP       |24.7  |46.2 |16.9 |65.0  |97.6  |0.34 |546  |178  |232  |136  |1796 |39348|1198 |1453 |62.3  |83.4  |63.4   |
|FRCNN     |21.0  |46.5 |13.6 |51.8  |97.2  |0.31 |546  |109  |261  |176  |1674 |54082|716  |810  |49.7  |88.2  |50.3   |

##### MOT16 Test Results
| Detector | Rcll | Prcn | FAR | GT  | MT  | PT  | ML  | FP  | FN  | IDs | FM  | MOTA | MOTP |
| -------- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- |
|SDP       |61.5  |95.2  |0.96 |759  |179  |330  |250  |5702 |70278|2167 |3028 |57.1  |77.1  |
|FRCNN     |50.9  |92.4  |1.29 |759  |113  |381  |265  |7639 |89535| 2284|2310 |45.4  |77.5  |

 Please note that this evaluation already includes the new ground truth of the MOT17 release.

## Contact
If you have any questions or encounter problems regarding the method/code feel free to contact me
at bochinski@nue.tu-berlin.de
