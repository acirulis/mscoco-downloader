from pycocotools.coco import COCO
import urllib.request
import os

dataDir = '.'
dataType = 'train2017'
annFile = '%s/annotations/instances_%s.json' % (dataDir, dataType)


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


coco = COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n\n', '; '.join(nms))

# get all images containing ALL given categories
catIds = coco.getCatIds(catNms=['truck'])
catIds_all = coco.getCatIds(catNms=['car', 'truck', 'bus', 'train'])
catNames = {0: 'car', 1: 'truck', 2: 'bus', 3: 'train'}
catMap = {3: 0, 6: 2, 7: 3, 8: 1}

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
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds_all, iscrowd=None)
        anns = coco.loadAnns(annIds)

        with open(ann_fname, "w", newline='\n') as text_file:
            for ann in anns:
                x = ann['bbox'][0]
                y = ann['bbox'][1]
                w = ann['bbox'][2]
                h = ann['bbox'][3]
                cx, cy, cw, ch = convert((img['width'], img['height']), (x, x + w, y, y + h))
                text_file.write('%s %s\n' % (catMap[ann['category_id']], ' '.join([str(x) for x in [cx, cy, cw, ch]])))
        print('%s downloaded (%s of %s) ' % (img['file_name'], cnt, len(imgIds)))
    cnt = cnt + 1
