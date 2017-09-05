print('COCO YOLO annotation translations')

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


ann_file = '000000033068.txt'
img_file = '000000033068.jpg'


with open('./coco/'+ann_file) as f:
    for line in f:  # Line is a string
        numbers_str = line.split()
        numbers_float = [float(x) for x in numbers_str]
        c, x,y,w,h = numbers_float
        cx,cy,cw,ch = convert((507, 640), (x,x+w,y, y+h))
        print(cx,cy,cw,ch)