import numpy as np
import os
import numpy as np
import nibabel as nib
import pydicom as dicom
import SimpleITK as sitk
from PIL import Image
import h5py

def makeIntoDicom(pixel_array):
  castFilter = sitk.CastImageFilter()
  castFilter.SetOutputPixelType(sitk.sitkInt16)

  img = sitk.GetImageFromArray(pixel_array)
  img = castFilter.Execute(img)

  # breakpoint()
  save_path = './' + f'result.dcm'
  sitk.WriteImage(img, save_path)
  print("dicom written at", save_path)
  print(slice_path)

def makeIntoImage(pixel_array):
  save_path = './'+"result.png"
  img = Image.fromarray(pixel_array.astype('int') , '1')
  img.save(save_path)
  print("Image written at", save_path)

W = 512
H = 512
debug = False






path_dicoms = 'raw_data'
path_labels = './raw_labels'

slices_num = sum([len(files) for r, d, files in os.walk(path_dicoms)])
train_num = int(slices_num * 0.8)
training_data = True
processed_imgs = 0

for dirpath, dirnames, filenames in os.walk(path_dicoms):
  if(len(filenames) == 0): continue
  if(processed_imgs > train_num): training_data = False
  tomography_number = dirpath.split('/')[1].split('_')[1]
  print ('Processing Tomography ' + tomography_number)
  label_filename = 'label' + tomography_number + '.nii'
  all_label_path = os.path.join(path_labels, label_filename)
  if(not os.path.isfile(all_label_path)): continue
  all_label_data = nib.load(all_label_path).get_fdata()
  test_image = []
  test_label = []
  if(debug):
    print('Dicom Label Path')
    print(all_label_path)
    print(all_label_path.shape)
  for slice_filename in filenames:
    # slice_number = int(slice_filename.split('-')[1].split('.')[0])
    slice_path = os.path.abspath(os.path.join(dirpath, slice_filename))
    dicom_info = dicom.dcmread(slice_path)
    if (dicom_info.pixel_array.shape[0] != W or dicom_info.pixel_array.shape[1] != H) :
      print(' %%%%%%%%%%%%%%%% SKIPPING: DICOM dicom_info does not fit ' + str(W) + 'x' + str(H) + ' size!')
      continue
    pixelData = dicom_info.PixelData
    slice_number = dicom_info.data_element("InstanceNumber").value
    dicom_data = np.frombuffer(pixelData, dtype=np.int16)
    dicom_data = np.reshape(dicom_data, (W,H))
    label_data = all_label_data[:,:,slice_number-1].T
    if(debug):
      unique, counts = np.unique(dicom_data, return_counts=True)
      occurences = dict(zip(unique, counts))
      print(dicom_data.shape)
      breakpoint()
    # makeIntoImage(label_data)
    # makeIntoDicom(label_data)

    if training_data:
      namefile = f"./train_npz/case{tomography_number}_slice{slice_number:03d}.npz"
      print('Saving at '+namefile)
      np.savez(namefile, image=dicom_data.astype(np.float32) / 1024, label=label_data.astype(np.uint8))
    else:
      test_image.append(dicom_data.astype(np.float32) / 1024)
      test_label.append(label_data.astype(np.float32))
    processed_imgs += 1
  if not training_data:
    print(f"Saving at test_vol_h5/case{tomography_number}.npy.h5")
    with h5py.File(f"./test_vol_h5/case{tomography_number}.npy.h5", 'a') as hdf5_file:
      hdf5_file.create_dataset('image', data=np.array(test_image))
      hdf5_file.create_dataset('label', data=np.array(test_label))
   