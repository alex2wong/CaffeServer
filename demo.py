#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib
matplotlib.use("Agg")
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel'),'sq':('ZF','sq_faster_rcnn_final.caffemodel')}


def vis_detections(im, class_name, dets, im_file, fw, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    im = im[:, :, (2, 1, 0)]
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
	fw.write("{\"obj\":[" + str(bbox[0]) +","+str(bbox[1])+","+str(bbox[2])+","+str(bbox[3])+"],")
	fw.write("\"class\": \"{:s}\",".format(class_name))
	fw.write("\"score\": {:3f}".format(score)) 
	fw.write("},")

def imageClassify(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the image uploaded by user..
    im_file = os.path.join('./assets', image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    fw = open(im_file+".txt", 'w')
    fw.write("{\"objects\": [\n")
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
#        fw.write("{extent:["+str(bbox[0])+","+str(bbox[1])+','+str(bbox[2])+","+str(bbox[3])+"],\n")
#        fw.write("class:" + class_name + ",\n")
#        fw.write("score:" + score + "},\n")

        vis_detections(im, cls, dets, im_file, fw, thresh=CONF_THRESH)
    fw.write("{}]}")
    fw.close()
#    cv2.imwrite('result_'+im_file, im)

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')

    args = parser.parse_args()

    return args

# if __name__ == '__main__':
    # fast_rcnn.config.cfg instance to config rcnn model.
cfg.TEST.HAS_RPN = True  # Use RPN for proposals

# args = parse_args()

# pt(layer cfg) and caffemodel is must to run model
prototxt = os.path.join(cfg.MODELS_DIR, NETS['zf'][0],
                        'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                            NETS['zf'][1])

if not os.path.isfile(caffemodel):
    raise IOError(('{:s} not found.\nDid you run ./data/script/'
                    'fetch_faster_rcnn_models.sh?').format(caffemodel))

if 1:
#if args.cpu_mode:
    caffe.set_mode_cpu()
else:
    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    cfg.GPU_ID = args.gpu_id
# create Net instance with caffe.Net(pt, model)
net = caffe.Net(prototxt, caffemodel, caffe.TEST)

print '\n\nLoaded network {:s}'.format(caffemodel)

# Warmup on a dummy image
im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
for i in xrange(2):
    _, _= im_detect(net, im)

#    im_names = ['000456.jpg', '000542.jpg', '001150.jpg',]
