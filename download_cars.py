from pycocotools.coco import COCO
import numpy as np
import matplotlib.pyplot as plt
import pylab
import urllib.request
import os

pylab.rcParams['figure.figsize'] = (10.0, 8.0)

dataDir = '.'
dataType = 'train2017'
annFile = '%s/annotations/instances_%s.json' % (dataDir, dataType)

coco = COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n\n', '; '.join(nms))


# get all images containing ALL given categories, select one at random
catIds = coco.getCatIds(catNms=['truck'])
imgIds = coco.getImgIds(catIds=catIds)
print('Total images found: ', len(imgIds))

imgs = coco.loadImgs(imgIds)

cnt = 1
for img in imgs:
    img_fname = '%s/images/%s' % (dataDir, img['file_name'])
    pre, ext = os.path.splitext(img_fname)
    ann_fname = pre + ".txt"
    if os.path.isfile(img_fname) and os.path.isfile(ann_fname):
        print('%s already exists' % img['file_name'])
    else:
        urllib.request.urlretrieve('http://mscoco.org/images/%d' % (img['id']), img_fname)
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)

        with open(ann_fname, "w", newline='\n') as text_file:
            for ann in anns:
                text_file.write('0 %s\n' % ' '.join([str(x) for x in ann['bbox']]))
        print('%s downloaded (%s of %s) ' % (img['file_name'], cnt, len(imgIds)))
    cnt = cnt + 1
