import numpy as np
import os
import numpy as np
import nibabel as nib
import pydicom as dicom
import SimpleITK as sitk
from PIL import Image
import h5py

path_train = './train_npz'
f_train = open("../../TransUNet/lists/list_NIH/train.txt", "w")

for dirpath, dirnames, filenames in os.walk(path_train):
  filenames.sort()
  for filename in filenames:
    f_train.write(f"{filename.split('.')[0]}\n")
f_train.close()

path_test = './test_vol_h5'
f_train = open("../../TransUNet/lists/list_NIH/test_vol.txt", "w")

for dirpath, dirnames, filenames in os.walk(path_test):
  filenames.sort()
  for filename in filenames:
    f_train.write(f"{filename.split('.')[0]}\n")
f_train.close()
