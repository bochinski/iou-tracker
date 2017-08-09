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
Several demo scripts are included to reproduce the reported results on the [UA-DETRAC](http://detrac-db.rit.albany.edu/)
and the [MOT](https://motchallenge.net/) 16/17 benchmarks.

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

Example for the MOT17-04 sequence (detections can be downloaded [here](https://motchallenge.net/data/MOT17/)):
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

Note that you still need a working python environment with numpy installed.
You should obtain something like the following results for the 'DETRAC-Train' set:

##### DETRAC-Train Results
| Detector | PR-Rcll | PR-Prcn | PR-FAR | PR-MT | PR-PT  | PR-ML | PR-FP   | PR-FN   | PR-IDs| PR-FM | PR-MOTA | PR-MOTP | PR-MOTAL |
| -------- | ------- | ------- | ------ | ----- | ------ | ----- | ------- | ------- | ----- | ----- | ------- | ------- | -------- |
| EB       |37.86    |44.73    |0.10    |32.34  |12.88   |20.93  |7958.82  |163739.85|4129.40|4221.89|35.77    |40.81    |36.48     |
| R-CNN    |27.86    |52.90    |0.11    |19.53  |17.03   |18.56  |9047.95  |157521.18|4842.18|4969.57|25.46    |44.39    |26.29     |
| CompACT  |25.15    |49.64    |0.09    |18.40  |14.15   |18.91  |7681.50  |152078.88|2177.44|2282.27|23.44    |42.88    |23.8191   |
| ACF      |27.39    |52.68    |0.14    |20.24  |15.66   |19.40  |11553.49 |161293.27|1845.49|2101.44|25.07    |44.71    |25.39     |

##### DETRAC-Test (Overall) Results
The reference results are taken from the [UA-DETRAC results](http://detrac-db.rit.albany.edu/TraRet) site. Only the best tracker / detector
combination is displayed for each reference method.

| Tracker       | Detector | PR-MOTA | PR-MOTP     | PR-MT     | PR-ML     | PR-IDs   | PR-FM    | PR-FP      | PR-FN      | Speed          |
| ------------- | -------- | ------- | ----------- | --------- | --------- | -------- | -------- | ---------- | ---------- | -------------- |
|CEM            | CompACT  | 5.1\%     |35.2\%     |3.0\%      |35.3\%     |**267.9** |**352.3** |**12341.2** |260390.4    |4.62 fps        |
|CMOT           | CompACT  | 12.6\%    |36.1\%     |16.1\%     |18.6\%     |285.3     |1516.8    |57885.9     |**167110.8**| & 3.79 fps     |
|GOG            | CompACT  | 14.2\%    |37.0\%     |13.9\%     |19.9\%     |3334.6    |3172.4    |32092.9     |180183.8    |390 fps         |
|DCT            | R-CNN    | 11.7\%    |38.0\%     |10.1\%     |22.8\%     |758.7     |742.9     |336561.2    |210855.6    |0.71 fps        |
|H<sup>2</sup>T | CompACT  | 12.4\%    |35.7\%     |14.8\%     |19.4\%     |852.2     |1117.2    |51765.7     |173899.8    | 3.02 fps       |
|IHTLS          | CompACT  | 11.1\%    |36.8\%     |13.8\%     |19.9\%     |953.6     |3556.9    |53922.3     |180422.3    |19.79 fps       |
|**IOU**        | R-CNN    |16.0\%     |**38.3\%** |13.8\%     |20.7\%     |5029.4    |5795.7    |22535.1     |193041.9    |**100,840 fps** |
|**IOU**        | EB       |**19.4\%** |28.9\%     |**17.7\%** |**18.4\%** |2311.3    |2445.9    |14796.5	  |171806.8    |6,902 fps       |

##### EB detections
The public detections of [EB](http://zyb.im/research/EB/) are not available on the
DETRAC training set and miss some low scoring detections. The EB detections we used for the tables above and our
publication are available here:

* [EB Train](https://tubcloud.tu-berlin.de/s/EtC6cFEYsAU0gFQ/download)
* [EB Test](https://tubcloud.tu-berlin.de/s/oKM3dYhJbMFl1dY/download)

### MOT17
The IOU Tracker was evaluated on the MOT17 benchmark as well. To determine the best parameters for each detector, an
exhaustive search of the parameter space was performed similar to the one of the MOT16 evaluation reported in the paper.
The best configuration for the training sequences is:

| Detector | ![sigma<sub>l<sub>](http://www.sciweavers.org/tex2img.php?eq=\sigma_l&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=)| ![sigma<sub>h</sub>](http://www.sciweavers.org/tex2img.php?eq=\sigma_{h}&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=) | ![sigma<sub>IOU</sub>](http://www.sciweavers.org/tex2img.php?eq=\sigma_{IOU}&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=) | ![t<sub>min</sub>](http://www.sciweavers.org/tex2img.php?eq=t_{min}&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=)      |
| -------- | ----------------- | ----------------- | ------------------- | -------------------- |
|DPM       | -0.5              | 0.5               | 0.4                 | 4                    |
|FRCNN     | 0.0               | 0.9               | 0.3                 | 3                    |
|SPD       | 0.4               | 0.5               | 0.2                 | 2                    |

To generate the MOT17 results listed at [MOT17 results](https://motchallenge.net/results/MOT17/), use the mot17.py script.
Note that the parameters from above are hard-coded in the script for your convenience.
```
usage: mot17.py [-h] -m SEQMAP -o RES_DIR -b BENCHMARK_DIR

IOU Tracker MOT17 demo script. The best parameters for each detector are
hardcoded.

optional arguments:
  -h, --help            show this help message and exit
  -m SEQMAP, --seqmap SEQMAP
                        full path to the seqmap file to evaluate
  -o RES_DIR, --res_dir RES_DIR
                        path to the results directory
  -b BENCHMARK_DIR, --benchmark_dir BENCHMARK_DIR
                        path to the sequence directory
```

Examples (you will probably need to adapt the paths):
```
./mot17.py -m ../motchallenge/seqmaps/c10-train.txt -o ../motchallenge/res/MOT17/iou-tracker -b ../data/mot17/train
./mot17.py -m ../motchallenge/seqmaps/c10-test.txt -o ../motchallenge/res/MOT17/iou-tracker -b ../data/mot17/test
```

##### MOT17 Train Results
| Detector | IDF1 | IDP | IDR | Rcll | Prcn | FAR | GT  | MT  | PT  | ML  | FP  | FN  | IDs | FM  | MOTA | MOTP | MOTAL |
| -------- | ---- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ----- |
|DPM       |14.3  |39.3 |8.7  | 35.8 | 88.1 | 1.02|546  |45   |195  |306  |5420 |72140|719  | 844 |  30.3|  77.1|  30.9 |
|FRCNN     |21.6  |47.5 |14.0 | 52.1 | 97.0 | 0.34|546  |111  |268  |167  |1804 |53774|857  | 876 |  49.7|  88.1|  50.5 |
|SDP       |24.4  |44.5 |16.8 | 66.8 | 96.8 | 0.47|546  |197  |240  |109  |2509 |37280|2058 | 2065|  62.7|  83.2|  64.6 |
|All       |9.9   |21.5 |6.4  | 51.6 | 94.7 | 0.61|1638 |353  |703  |582  |97331|63194|3634 | 3785|  47.6|  83.4|  48.7 |

##### MOT17 Test Results
| MOTA | MOTP |	FAF	| MT    | ML    | FP    | FN     | ID Sw. | Frag |
| ---- | ---- | --- | ----- | ----- | ----- | ------ | ------ | ---- |
| 45.5 |76.9  |1.1	|15.7\% |40.5\% |19,993	|281,643 | 5,988  |7,404 |

### MOT16
To reproduce the reported [MOT16 results](https://motchallenge.net/results/MOT16/) of the paper, use the mot16.py script:

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

Examples (you will probably need to adapt the paths):
```
# SDP:
./mot16.py -m ../motchallenge/seqmaps/sdp-train.txt -o ../motchallenge/res/MOT16/iou-tracker -b ../data/mot17/train

# FRCNN:
./mot16.py -m ../motchallenge/seqmaps/frcnn-train.txt -o ../motchallenge/res/MOT16/iou-tracker -b ../data/mot17/train -sl 0 -sh 0.9 -si 0.3 -tm 5
```

The seqmap files can be found under "seqmaps" and need to be copied to the respective directory of the
motchallenge devkit.
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
