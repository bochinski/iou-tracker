## IOU Tracker
Python implementation of the IOU/V-IOU Tracker described in the AVSS 2017/2018 papers:

[High-Speed Tracking-by-Detection Without Using Image Information](http://elvera.nue.tu-berlin.de/files/1517Bochinski2017.pdf)

[Extending IOU Based Multi-Object Tracking by Visual Information](http://elvera.nue.tu-berlin.de/files/1547Bochinski2018.pdf)

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

@INPROCEEDINGS{1547Bochinski2018,
	AUTHOR = {Erik Bochinski and Tobias Senst and Thomas Sikora},
	TITLE = {Extending IOU Based Multi-Object Tracking by Visual Information},
	BOOKTITLE = {IEEE International Conference on Advanced Video and Signals-based Surveillance},
	YEAR = {2018},
	MONTH = nov,
	PAGES = {441--446},
	ADDRESS = {Auckland, New Zealand},
	URL = {http://elvera.nue.tu-berlin.de/files/1547Bochinski2018.pdf}
}
```
### Table Of Contents
- [Install](#Install)
- [Demo](#Demo)
- [DETRAC](#DETRAC)
- [Motchallenge](#Motchallenge)
  * [MOT16](#MOT16)
  * [MOT17](#MOT17)
  * [CVPR19](#CVPR19)
- [Visdrone-MOT](#Visdrone-MOT)
- [Contact](#Contact)

**Update** (Jan 2020):
* added V-IOU Code
* updated README.md

**Update** (December 2018):
* added V-IOU results of our new paper [Extending IOU Based Multi-Object Tracking by Visual Information](http://elvera.nue.tu-berlin.de/files/1547Bochinski2018.pdf)
* Mask R-CNN detections for UA-DETRAC added
* CompACT parameters improved

### Install
The repository now contains the code for both the IOU tracker and the V-IOU tracker.
The IOU Tracker only depends on numpy while V-IOU also requires OpenCV-Contrib and some other dependencies.
It is recommended to use a virtual environment to run the code:
```
virtualenv -p python3 env
source env/bin/activate
pip install numpy lapsolver tqdm opencv-contrib-python
```
This should get you started with a basic installation to run most the scripts in this repository.

#### KCF/KCF2
Two different implementations of the KCF visual tracker can be used. One is supplied by OpenCV-Contrib and is denoted as *KCF*. This one should work out of the box.
The second implementation is denoted as *KCF2*. This one is needed to reproduce the reported results. In order to use this you need to install [KCFcpp-py-wrapper](https://github.com/uoip/KCFcpp-py-wrapper),
which is a Cython based wrapper of the original KCF code for python.
It is recommended to build and install OpenCV from scratch instead of using the PyPI package in order to have all the necessary headers and libraries available.

Why? Because this implementation seems to work better and much faster than the one provided by OpenCV-Contrib. 

If you do not install this module the tracker will automatically fall back on the OpenCV implementation (i.e. *KCF*) and a warning is printed. 
You can get rid of this warning by either by installing the other KCF module as described above or explicitly request *KCF* instead of *KCF2* in the scripts. 
Note that the tracking performance will be affected by this.


### Demo
Several demo scripts are included to reproduce the reported results on the [UA-DETRAC](http://detrac-db.rit.albany.edu/)
, [MOT](https://motchallenge.net/) 16/17/19 and [VisDrone](http://www.aiskyeye.com/)  benchmarks.

Basic demo script (not dataset specific, can be used for other applications):
```
$ ./demo.py -h
usage: demo.py [-h] [-v VISUAL] [-hr KEEP_UPPER_HEIGHT_RATIO] [-f FRAMES_PATH]
               -d DETECTION_PATH -o OUTPUT_PATH [-sl SIGMA_L] [-sh SIGMA_H]
               [-si SIGMA_IOU] [-tm T_MIN] [-ttl TTL] [-nms NMS] [-fmt FORMAT]

IOU/V-IOU Tracker demo script

optional arguments:
  -h, --help            show this help message and exit
  -v VISUAL, --visual VISUAL
                        visual tracker for V-IOU. Currently supported are
                        [BOOSTING, MIL, KCF, KCF2, TLD, MEDIANFLOW, GOTURN,
                        NONE] see README.md for furthert details
  -hr KEEP_UPPER_HEIGHT_RATIO, --keep_upper_height_ratio KEEP_UPPER_HEIGHT_RATIO
                        Ratio of height of the object to track to the total
                        height of the object for visual tracking. e.g. upper
                        30%
  -f FRAMES_PATH, --frames_path FRAMES_PATH
                        sequence frames with format
                        '/path/to/frames/frame_{:04d}.jpg' where '{:04d}' will
                        be replaced with the frame id. (zero_padded to 4
                        digits, use {:05d} for 5 etc.)
  -d DETECTION_PATH, --detection_path DETECTION_PATH
                        full path to CSV file containing the detections
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        output path to store the tracking results (MOT
                        challenge/Visdrone devkit compatible format)
  -sl SIGMA_L, --sigma_l SIGMA_L
                        low detection threshold
  -sh SIGMA_H, --sigma_h SIGMA_H
                        high detection threshold
  -si SIGMA_IOU, --sigma_iou SIGMA_IOU
                        intersection-over-union threshold
  -tm T_MIN, --t_min T_MIN
                        minimum track length
  -ttl TTL, --ttl TTL   time to live parameter for v-iou
  -nms NMS, --nms NMS   nms for loading multi-class detections
  -fmt FORMAT, --format FORMAT
                        format of the detections [motchallenge, visdrone]
```

Example for the IOU tracker on the MOT17-04 sequence (detections can be downloaded [here](https://motchallenge.net/data/MOT17/)):
```
./demo.py -d ../mot17/train/MOT17-04-SDP/det/det.txt -o res/iou-tracker/MOT17-04-SDP.txt
```

Example for the V-IOU tracker on the uav0000137_00458_v Visdrone sequence:
```
demo.py -f '/path/to/VisDrone2018-MOT-val/sequences/uav0000137_00458_v/{:07d}.jpg' -d /path/to/VisDrone2018-MOT-val/detections/uav0000137_00458_v.txt -o results/VisDrone2018-MOT-val/uav0000137_00458_v.txt -v MEDIANFLOW -sl 0.9 -sh 0.98 -si 0.1 -tm 23 --ttl 8 --nms 0.6 -fmt visdrone
```

### DETRAC
To reproduce the reported results, download and extract the [DETRAC-toolkit](http://detrac-db.rit.albany.edu/download)
and the detections you want to evaluate. Download links for the EB and Mask R-CNN detections are provided below.
Clone this repository into "DETRAC-MOT-toolkit/trackers/".
Follow the instructions to configure the toolkit for tracking evaluation and set the tracker name in "DETRAC_experiment.m":

```
tracker.trackerName = 'iou-tracker';
```

and run the script.
You can switch between IOU and V-IOU and select the different parameters for different detectors in run_tracker.m 

Note that you still need a working python environment with numpy for IOU and all other dependencies for V-IOU installed.
You should obtain something like the following results for the 'DETRAC-Train' set:

##### DETRAC-Train Results
IOU Tracker:

| Detector   | PR-Rcll | PR-Prcn | PR-FAR | PR-MT | PR-PT  | PR-ML | PR-FP   | PR-FN   | PR-IDs| PR-FM | PR-MOTA | PR-MOTP | PR-MOTAL |
| --------   | ------- | ------- | ------ | ----- | ------ | ----- | ------- | ------- | ----- | ----- | ------- | ------- | -------- |
| EB         |37.86    |44.73    |0.10    |32.34  |12.88   |20.93  |7958.82  |163739.85|4129.40|4221.89|35.77    |40.81    |36.48     |
| R-CNN      |27.86    |52.90    |0.11    |19.53  |17.03   |18.56  |9047.95  |157521.18|4842.18|4969.57|25.46    |44.39    |26.29     |
| CompACT    |25.20    |49.69    |0.10    |18.50  |14.11   |19.06  |8053.54  |153026.99|2021.84|2302.83|23.46    |42.96    |23.81     |
| ACF        |27.39    |52.68    |0.14    |20.24  |15.66   |19.40  |11553.49 |161293.27|1845.49|2101.44|25.07    |44.71    |25.39     |
| Mask R-CNN |43.21    |47.26    |0.60    |37.22  |11.46   |24.24  |50096.88 |171714.09|1021.94|929.53 |34.36    |45.43    |34.54     |

V-IOU Tracker:

| Detector   | PR-Rcll | PR-Prcn | PR-FAR | PR-MT | PR-PT  | PR-ML | PR-FP   | PR-FN   | PR-IDs| PR-FM | PR-MOTA | PR-MOTP | PR-MOTAL |
| --------   | ------- | ------- | ------ | ----- | ------ | ----- | ------- | ------- | ----- | ----- | ------- | ------- | -------- |
| CompACT    |26.84    |49.57    |0.10    |19.63  |14.67   |17.39  |8750.71  |143532.90|244.98 |444.20 |25.29    |41.58    |25.33     |
| Mask R-CNN |42.80    |47.50    |0.60    |38.32  |8.36    |26.24  |50294.76 |174052.00|448.16 |293.69 |34.02    |46.87    |34.10     |


##### DETRAC-Test (Overall) Results
The reference results are taken from the [UA-DETRAC results](http://detrac-db.rit.albany.edu/TraRet) site. Only the best tracker / detector
combination is displayed for each reference method.

| Tracker       | Detector    | PR-MOTA | PR-MOTP     | PR-MT     | PR-ML     | PR-IDs   | PR-FM    | PR-FP      | PR-FN      | Speed          |
| ------------- | ----------- | ------- | ----------- | --------- | --------- | -------- | -------- | ---------- | ---------- | -------------- |
|CEM            | CompACT     | 5.1\%     |35.2\%     |3.0\%      |35.3\%     |267.9     |352.3     |**12341.2** |260390.4    |4.62 fps        |
|CMOT           | CompACT     | 12.6\%    |36.1\%     |16.1\%     |18.6\%     |285.3     |1516.8    |57885.9     |167110.8    |3.79 fps        |
|GOG            | CompACT     | 14.2\%    |37.0\%     |13.9\%     |19.9\%     |3334.6    |3172.4    |32092.9     |180183.8    |390 fps         |
|DCT            | R-CNN       | 11.7\%    |38.0\%     |10.1\%     |22.8\%     |758.7     |742.9     |336561.2    |210855.6    |0.71 fps        |
|H<sup>2</sup>T | CompACT     | 12.4\%    |35.7\%     |14.8\%     |19.4\%     |852.2     |1117.2    |51765.7     |173899.8    |3.02 fps        |
|IHTLS          | CompACT     | 11.1\%    |36.8\%     |13.8\%     |19.9\%     |953.6     |3556.9    |53922.3     |180422.3    |19.79 fps       |
|**IOU**        | R-CNN    |16.0\%        |**38.3\%** |13.8\%     |20.7\%     |5029.4    |5795.7    |22535.1     |193041.9    |100,840 fps     |
|**IOU**        | EB       |19.4\%        |28.9\%     |17.7\%     |**18.4\%** |2311.3    |2445.9    |14796.5	  |171806.8   |6,902 fps       |
|**IOU**        | CompACT     | 16.1\%    |37.0\%     |14.8\%     |19.7\%     |2308.1    |3250.4    |24349.4     |176752.8    |**327,660 fps** |
|**IOU**        | Mask R-CNN  | **30.7\%**|37.0\%     |30.3\%     |21.5\%     |668.0     |733.6     |17370.3     |179505.9    |14,956 fps      |
|**V-IOU**      | CompACT     | 17.7\%    |36.4\%     |17.4\%     |18.8\%     |363.8     |1123.5    |26413.3     |**166571.7**|1117.90fps      |
|**V-IOU**      | Mask R-CNN  | **30.7\%**|37.0\%     |**32.0\%** |22.6\%     |**162.6** |**286.2** |18046.2     |179191.2    |359.18 fps      |

##### EB detections
The public detections of [EB](http://zyb.im/research/EB/) are not available on the
DETRAC training set and miss some low scoring detections. The EB detections we used for the tables above and our
publication are available here:

* [EB Train](https://tubcloud.tu-berlin.de/s/EtC6cFEYsAU0gFQ/download)
* [EB Test](https://tubcloud.tu-berlin.de/s/oKM3dYhJbMFl1dY/download)

##### Mask R-CNN detections
These detections are generated using a recent Mask R-CNN implementation trained on COCO.
Only bounding boxes for COCOs *car*, *bus* and *truck* classes are included.
Note that the detector is called "frcnn" (use `options.detectorSet = {'frcnn'};` in *initialize_environment.m*).
* [Mask R-CNN Train](https://tubcloud.tu-berlin.de/s/MnGRGdH98WY9xQr/download)
* [Mask R-CNN Test](https://tubcloud.tu-berlin.de/s/EztsFgm5AL8Jwtt/download)

## Motchallenge

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


### MOT17
The IOU Tracker was evaluated on the MOT17 benchmark as well. To determine the best parameters for each detector, an
exhaustive search of the parameter space was performed similar to the one of the MOT16 evaluation reported in the paper.
The best configuration for the training sequences is:

| Detector | ![sigma_l](http://latex.codecogs.com/gif.latex?\sigma_l)| ![sigma_h](http://latex.codecogs.com/gif.latex?\sigma_h) | ![sigma_iou](http://latex.codecogs.com/gif.latex?\sigma_{IOU}) | ![t_min](http://latex.codecogs.com/gif.latex?t_{min})      |
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


### CVPR19
To reproduce the results on the CVPR19 dataset you can use the cvpr19.sh bash script. 

Edit the first lines according to your setup:
```
# set these variables according to your setup
seq_dir=/path/to/cvpr19/train # base directory of the split (cvpr19/train, cvpr19/test etc.)
results_dir=results/cvpr19    # output directory, will be created if not existing
```
Then, run (The used parameters for the *demo.py* script will be displayed for your convenience):
```
./cvpr19.sh
```

Note that this requires to have *KCF2* tracker installed.

Note that only the upper 30% of the detections are used for visual tracking since the bottom part is often occluded.
Due to time constraints only *KCF2* was evaluated for the CVPR19 challenge participation, 
*MEDIANFLOW* might yield better results like for the [Visdrone-MOT](#Visdrone-MOT) experiments but additional parameter tuning is required.

##### CVPR19 Train Results
| Detector | IDF1 | IDP | IDR | Rcll | Prcn | FAR | GT  | MT  | PT  | ML  | FP  | FN  | IDs | FM  | MOTA | MOTP | MOTAL |
| -------- | ---- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ----- |
| FRCNN    | 53.9 | 71.6| 43.2| 59.9 | 99.3 | 0.63| 2274| 670 |1187 | 417 |55844|97170| 3272|4792 | 59.2 | 87.5 | 59.5  |

### Visdrone-MOT
To reproduce the results on the Visdrone MOT dataset you can use the visdrone-mot.sh bash script.
Edit the first lines according to your setup:
```
# set these variables according to your setup
visdrone_dir=/path/to/VisDrone2018-MOT-val  # base directory of the split (VisDrone2018-MOT-val, VisDrone2018-MOT-train etc.)
results_dir=results/VisDrone2018-MOT-val    # output directory, will be created if not existing
vis_tracker=MEDIANFLOW                      # [MEDIANFLOW, KCF2, NONE] parameter set as used in the paper
```
Then, run (The used parameters for the *demo.py* script will be displayed for your convenience):
```
./visdrone-mot.sh
```

##### Visdrone-MOT Val Results
For the *VisDrone2018-MOT-val* split you should get the following results:

| Visual Tracker | IDF1 | IDP | IDR | Rcll | Prcn | FAR | GT  | MT  | PT  | ML  | FP  | FN  | IDs | FM  | MOTA | MOTP | MOTAL |
| -------------- | ---- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ----- |
| None           | 40.9 | 68.5| 29.2| 34.6 | 81.3 | 0.60| 476 | 102 | 76  | 297 | 5736|46979| 177 | 435 | 26.4 | 78.1 | 26.6  |
| KCF            | 45.3 | 75.3| 32.4| 35.2 | 81.8 | 0.59| 476 | 105 | 64  | 305 | 5605|46578| 76  | 385 | 27.3 | 77.9 | 27.4  |
| Medianflow     | 45.6 | 75.9| 32.6| 35.3 | 82.2 | 0.58| 476 | 107 | 63  | 304 | 5494|46466| 65  | 378 | 27.6 | 77.8 | 27.7  |


## Contact
If you have any questions or encounter problems regarding the method/code feel free to contact me
at bochinski@nue.tu-berlin.de
