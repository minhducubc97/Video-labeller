import xml.etree.ElementTree as ET
import glob
from xml.dom import minidom
import os
import shutil

# convert xml to readable file
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# clear all files in folder
def clearFolder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

# clear frames and labels folder
clearFolder('labels/')

# get the list of images
imageList = glob.glob('frames/*.png')
print(imageList)

# open annotation files
face = open('face_annot.txt', 'r')
person = open('person_annot.txt', 'r')

# grab the all necessary info from face_annot.txt
currLine_face = face.readline()
currArray_face = currLine_face.split(',')
currFrame_face = int(currArray_face[0].split(':')[1])
currXMin_face = currArray_face[1].split(':')[1]
currXMax_face = currArray_face[2].split(':')[1]
currYMin_face = currArray_face[3].split(':')[1]
currYMax_face = currArray_face[4].split(':')[1]

# grab the all necessary info from person_annot.txt
currLine_person = person.readline()
currArray_person = currLine_person.split(',')
currFrame_person = int(currArray_person[0].split(':')[1])
currXMin_person = currArray_person[1].split(':')[1]
currXMax_person = currArray_person[2].split(':')[1]
currYMin_person = currArray_person[3].split(':')[1]
currYMax_person = currArray_person[4].split(':')[1]

counter = 1
stopReadingFace = False
stopReadingPerson = False

# construct the xml files
for img in imageList:
    imgName = img.split('\\')[1]
    annotation = ET.Element('annotation')
    folder = ET.SubElement(annotation, 'folder').text = 'Images'
    filename = ET.SubElement(annotation, 'filename').text = imgName
    path = ET.SubElement(annotation, 'path').text = '/output/Images/' + imgName
    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database').text = 'Unknown'
    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width').text = '720'
    height = ET.SubElement(size, 'height').text = '540'
    depth = ET.SubElement(size, 'depth').text = '3'
    segmented = ET.SubElement(annotation, 'segmented').text = '0'

    while (currFrame_face == counter and stopReadingFace == False):
        theObject = ET.SubElement(annotation, 'object')
        name = ET.SubElement(theObject, 'name').text = 'face'
        pose = ET.SubElement(theObject, 'pose').text = 'Unspecified'
        truncated = ET.SubElement(theObject, 'truncated').text = '0'
        difficult = ET.SubElement(theObject, 'difficult').text = '0'
        bndbox = ET.SubElement(theObject, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin').text = currXMin_face
        xmax = ET.SubElement(bndbox, 'xmax').text = currXMax_face
        ymin = ET.SubElement(bndbox, 'ymin').text = currYMin_face
        ymax = ET.SubElement(bndbox, 'ymax').text = currYMax_face

        currLine_face = face.readline()
        currArray_face = currLine_face.split(',')
        if len(currArray_face) != 5:
            stopReadingFace = True
            break
        else:
            currFrame_face = int(currArray_face[0].split(':')[1])
            currXMin_face = currArray_face[1].split(':')[1]
            currXMax_face = currArray_face[2].split(':')[1]
            currYMin_face = currArray_face[3].split(':')[1]
            currYMax_face = currArray_face[4].split(':')[1]

    while (currFrame_person == counter and stopReadingPerson == False):
        theObject = ET.SubElement(annotation, 'object')
        name = ET.SubElement(theObject, 'name').text = 'person'
        pose = ET.SubElement(theObject, 'pose').text = 'Unspecified'
        truncated = ET.SubElement(theObject, 'truncated').text = '0'
        difficult = ET.SubElement(theObject, 'difficult').text = '0'
        bndbox = ET.SubElement(theObject, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin').text = currXMin_person
        xmax = ET.SubElement(bndbox, 'xmax').text = currXMax_person
        ymin = ET.SubElement(bndbox, 'ymin').text = currYMin_person
        ymax = ET.SubElement(bndbox, 'ymax').text = currYMax_person

        currLine_person = person.readline()
        currArray_person = currLine_person.split(',')
        if len(currArray_person) != 5:
            stopReadingPerson = True
            break
        else:
            currFrame_person = int(currArray_person[0].split(':')[1])
            currXMin_person = currArray_person[1].split(':')[1]
            currXMax_person = currArray_person[2].split(':')[1]
            currYMin_person = currArray_person[3].split(':')[1]
            currYMax_person = currArray_person[4].split(':')[1]
    
    output = prettify(annotation).split('\n', 1)[1]
    file = open('labels/' + str(imgName.split('.')[0]) + '.xml', 'w+')
    file.write(output)
    file.close()

    if (currFrame_face > counter and currFrame_person > counter):
        counter += 1

face.close()
person.close()