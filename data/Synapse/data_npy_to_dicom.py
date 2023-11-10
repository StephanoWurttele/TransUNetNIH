from PIL import Image
import numpy as np
import SimpleITK as sitk
import pdb
import os

# case0005_slice000.npz
save_dir = './dicom_data/'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

test = np.load('train_npz/case0005_slice039.npz')
# test = np.load('out.npz')
breakpoint()
for data in test:
  print(data)
  print(test[data])
breakpoint()
data_image = test['image'] * 255
# FOR IMAGE
img = Image.fromarray(data_image.astype('uint8') , 'L')
img.save(save_dir+"result.png")

# FOR DICOM
castFilter = sitk.CastImageFilter()
castFilter.SetOutputPixelType(sitk.sitkUInt8)

img = sitk.GetImageFromArray(data_image)
img = castFilter.Execute(img)

# breakpoint()
save_path = save_dir + f'result.dcm'
sitk.WriteImage(img, save_path)
print("dicom written at", save_path)











# dcm = "PANCREAS_0013"
# sliceNum = "75"
# data_path = "train_npz/"

# data_npy = data_path + "originalDcmValues.npy"
# print("Will project segmentation on dicom in ", real_dcm_npy_path)
# intSliceNum = (int(sliceNum))
# real_dcm_npy = np.load(real_dcm_npy_path)
# real_dcm_npy_slice = real_dcm_npy[intSliceNum]

# def color_border():
#     for i in range(512):
#         for j in range(512):
#             if(outlined_segment_npy[i][j] == 255):
#                 real_dcm_npy_slice[i][j] = 2000

# color_border()

# ints = 16

# castFilter = sitk.CastImageFilter()
# castFilter.SetOutputPixelType(sitk.sitkInt16)

# img = sitk.GetImageFromArray(real_dcm_npy_slice)
# real_dcm_npy_slice = castFilter.Execute(img)

# save_path = dcm_path + f'results_in_dicom_test1_{ints}.dcm'
# sitk.WriteImage(real_dcm_npy_slice, save_path)
# print("dicom written at", save_path)
