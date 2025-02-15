#!/usr/bin/python
# Matthew Dunlop, August 2018
# https://github.com/mdunlop2
#
# Contact:
# https://www.linkedin.com/in/mdunlop2/

'''
## Tflite Object Detection
Currently, `python-tflite.py` supports using Mobilenet-V1 SSD models trained using Cloud Annotations.

Note: to find a list of all models trained do:
```
cacli list
```

To use a custom model, perform
```
cacli download <model_name>
```
For example, if the downloaded files were saved to `/path/to/<model_name>` :
* Our tflite model is stored in `<model_name>/model_android/model.tflite`
* Our tflite anchors file is stored in `<model_name>/model_android/anchors.json`
* Our tflite labels file is stored in `<model_name>/model_android/labels.json`

Change directory to the root of this git.
```
cd examples/tflite_interpreter/basic/
python python-tflite.py --MODEL_DIR /path/to/<model_name>/model_android
```
This script calls the tflite model interpreter for inference on all .jpg files inside the directory `PATH_TO_TEST_IMAGES_DIR`.

Similary the output .jpg files are storesd in `PATH_TO_OUTPUT_DIR`.

We can also specify the minimum confidence (score) for a given detection box to be displayed with `MINIMUM_CONFIDENCE`.

Finally:
```
python python-tflite.py \
--MODEL_DIR /path/to/<model_name>/model_android \
--PATH_TO_TEST_IMAGES_DIR /path/to/test/images \
--PATH_TO_OUTPUT_DIR /path/to/output/images \
--MINIMUM_CONFIDENCE 0.01

```
'''
import glob
import os

import argparse

# from examples.tflite_interpreter.basic.utils import visualization_utils as vis_util
# from examples.tflite_interpreter.basic.utils import cacli_models as models
from utils import visualization_utils as vis_util
from utils import cacli_models as models


# Directory in which this example takes place
EXAMPLE_DIR = os.getcwd()

# Optional User Inputs
parser = argparse.ArgumentParser(description='Perform cacli tflite model inference')
parser.add_argument('--MODEL_DIR', default = EXAMPLE_DIR + "/model/sample_model",
                   help='Give the path to your folder containing model.tflite, anchors.json and labels.json')

parser.add_argument('--MINIMUM_CONFIDENCE', default = 0.01,
                   help='Minimum score for an object to be considered for plotting')

parser.add_argument('--PATH_TO_TEST_IMAGES_DIR', default = EXAMPLE_DIR + "/model/test_images",
                   help='Path to folder containing images (.jpg) to test model on')

parser.add_argument('--PATH_TO_OUTPUT_DIR', default = EXAMPLE_DIR + "/model/output",
                   help='Path to folder where model will place output images')

a = parser.parse_args()

TEST_IMAGE_PATHS = glob.glob(os.path.join(a.PATH_TO_TEST_IMAGES_DIR, '*.jpg'))
MODEL_PATH = a.MODEL_DIR + "/model.tflite"
MODEL_ANCHOR_PATH = a.MODEL_DIR + "/anchors.json"
MODEL_LABEL_PATH = a.MODEL_DIR + "/labels.json"

print(a.MODEL_DIR)
# Load model and allocate tensors
model_interpreter = models.initiate_tflite_model(MODEL_PATH)
# Load mobilenet-v1 anchor points
anchor_points = models.json_to_numpy(MODEL_ANCHOR_PATH)

# Load Category Index
label_list = models.json_to_numpy(MODEL_LABEL_PATH)

category_index = { i : {"name" : label_list[i]} for i in list(range(len(label_list))) }
count= 0
for image_path in TEST_IMAGE_PATHS:
  count += 1
  print("\nImage {} of {}.".format(count,len(TEST_IMAGE_PATHS)+1))
  models.detect_objects(model_interpreter,
                        image_path,
                        category_index,
                        anchor_points,
                        a.MINIMUM_CONFIDENCE,
                        SAVE_DIR=a.PATH_TO_OUTPUT_DIR)
