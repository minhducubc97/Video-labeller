# Video Labeller
A video labeller that can track multiple objects using bounding box throughout the video and output xml file in Pascal VOC format for each corresponding frame.

## How to use
In the terminal, run:
```
python labeller.py --video /PATH/TO/VIDEO --tracker TRACKER_TYPE --annot /PATH/TO/ANNOTATION/FILE 
```
where there are 3 input parameters:
- video: path to the video file to label
- tracker: type of tracker for track objects. There are seven types of trackers: 
    + csrt: A bit slow but very accurate (recommended)
    + kcf: Averagely fast and averagely accurate
    + boosting: Slow and not very accurate
    + mil: Averagely accurate, but handle errors badly
    + tld: Prone to false-positive (not recommended)
    + medianflow: Averagely accurate only if the video is slow
    + mosse: Extremely fast but not very accurate -> good when user needs for speed
    + goturn: Extremely fast but not very accurate -> good when user needs for speed
    By default, csrt is used.
- annot: path to the annotation file

## Specifications:
The project uses OpenCV Object Tracker.