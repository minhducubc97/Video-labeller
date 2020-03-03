# Video Labeller
A video labeller that can track multiple objects using bounding box throughout the video and output xml file in Pascal VOC format for each corresponding frame.

## How to use
In the terminal, run:
```
python labeller.py --video /PATH/TO/VIDEO --tracker TRACKER_TYPE --annot /PATH/TO/ANNOTATION/FILE 
```
where there are 3 input parameters:
- video: path to the video file to label
- tracker: type of tracker for track objects. There are seven types of trackers: csrt, kcf, boosting, mil, tld, medianflow, mosse, goturn. By default, csrt is used.
- annot: path to the annotation file

## Specifications:
The project uses OpenCV Object Tracker.