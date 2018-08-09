import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# %matplotlib inline
import time
import math
from nms import nms
from crop_image import crop_image
from utils import *

# Make sure that caffe is on the python path:
caffe_root = './'  # this file is expected to be in {caffe_root}/examples
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

import caffe
caffe.set_device(0)
caffe.set_mode_gpu()


config = {
	'model_def' : './models/deploy.prototxt',
	'model_weights' : './models/model_icdar15.caffemodel',
	'img_dir' : './demo_images/',
	'image_name' : 'demo.jpg',
	'det_visu_path' : './demo_images/demo_det_result.jpg',
	'rec_visu_path' : './demo_images/demo_rec_result.jpg',
	'det_save_dir' : './demo_images/detection_result/',
	'rec_save_dir' : './demo_images/recognition_result/',
	'crop_dir' : './demo_images/crops/',
	'lexicon_path' : './crnn/data/icdar_generic_lexicon.txt',
	'use_lexcion' : True,
	'input_height' : 768,
	'input_width' : 768,
	'overlap_threshold' : 0.2,
	'det_score_threshold' : 0.1,
	'f_score_threshold' : 0.7,
	'visu_detection' : True,
	'visu_recognition': True,
	'apply_recognition' : True
}



# detection
print("detection")
print("  prepare network")
net = prepare_network(config)
print("  create transformer")
transformer =  create_transformer(config)
print("  process image")
path = os.path.join(config['img_dir'], config['image_name'])
width = config['input_width']
height = config['input_height']
image, detections = process_image(net, transformer, path, width, height)


# Parse the outputs.
print("  extract stuff")
image_height, image_width, channels=image.shape
bboxes = extract_detections(detections, config['det_score_threshold'], image_height, image_width)
# apply non-maximum suppression
results = apply_quad_nms(bboxes, config['overlap_threshold'])
save_and_visu(image, results, config)
print('detection finished')
print()

# recognition
if config['apply_recognition']:
	print('recognition begin')
	# crop 
	crop_image(os.path.join(config['img_dir'], config['image_name']), results, config['crop_dir'])
	import subprocess
	if config['use_lexcion']:
		subprocess.check_call(['th', 'crnn/src/demo.lua', '-imgDir', config['img_dir'],\
	 		'-imgName', config['image_name'], '-cropDir', config['crop_dir'], '-resultDir', config['rec_save_dir'],\
	 		'-dicPath', config['lexicon_path']])
	else:
		subprocess.check_call(['th', 'crnn/src/demo.lua', '-imgDir', config['img_dir'],\
	 		'-imgName', config['image_name'], '-cropDir', config['crop_dir'], '-resultDir', config['rec_save_dir'],\
	 		'-dicPath', config['lexicon_path']])
if config['visu_recognition']:
	visu_rec_results(image, config['rec_save_dir'], config['f_score_threshold'], config)
	
