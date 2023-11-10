from PIL import Image
import numpy as np
import SimpleITK as sitk
import pdb
import os

# case0005_slice000.npz
save_dir = './dicom_data/'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

test = np.load('train_npz/case0013_slice129.npz')
# test = np.load('out.npz')
for data in test:
  print(data)
# breakpoint()
image = test['image'] * 1024
label = test['label']

# FOR DICOM
castFilter = sitk.CastImageFilter()
castFilter.SetOutputPixelType(sitk.sitkInt16)

img = sitk.GetImageFromArray(image)
img = castFilter.Execute(img)

save_path = save_dir + f'image-result.dcm'
sitk.WriteImage(img, save_path)
print("image written at", save_path)

img = sitk.GetImageFromArray(label)
img = castFilter.Execute(img)

save_path = save_dir + f'label-result.dcm'
sitk.WriteImage(img, save_path)
print("image written at", save_path)

