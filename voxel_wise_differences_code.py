import nibabel as nib
import numpy as np
import os

group1_files = [
    'sub1.nii','sub2.nii','sub3.nii','sub4.nii','sub5.nii',
    'sub6.nii','sub7.nii','sub8.nii','sub9.nii','sub10.nii'
]
group2_files = [
    'sub11.nii','sub12.nii','sub13.nii','sub14.nii','sub15.nii',
    'sub16.nii','sub17.nii','sub18.nii','sub19.nii','sub20.nii',
]

# Load images 
voxel1_data = []
for file in group1_files:
    img = nib.load(file) # this doesnt load voxel intensities in memory yet
    img_voxel = img.get_fdata() # img.get_fdata() loads the voxel data
    voxel1_data.append(img_voxel) 

voxel2_data = []
for file in group2_files:
    img = nib.load(file) # this doesnt load voxel intensities in memory yet
    img_voxel = img.get_fdata()
    voxel2_data.append(img_voxel) 
    
# convert to numpy array with 4D
group1_voxel = np.stack(voxel1_data, axis =- 1)
group2_voxel = np.stack(voxel2_data, axis =- 1)

# t-test 
import scipy.stats as stats

# print(group1_voxel.shape)

t_stats = np.zeros(group1_voxel.shape[:3])
p_values = np.zeros(group1_voxel.shape[:3])

for i in range(91):
    for j in range(109):
        for k in range(91):
            group1 = group1_voxel[i, j, k, :] # will return the voxel at this coordiate for each sub in group1
            group2 = group2_voxel[i, j, k, :]
            t_stat, p_value = stats.ttest_ind(a=group1, b=group2, equal_var=True)

            t_stats[i, j, k] = t_stat
            p_values[i, j, k] = p_value


# threshold t-test results
threshold1 = p_values < .05
threshold2 = p_values < .01
threshold3 = p_values < .001

mask1 = np.array(threshold1, dtype=np.int16)
mask2 = np.array(threshold2, dtype=np.int16)
mask3 = np.array(threshold3, dtype=np.int16)

# save results as .nii files
img_t = nib.Nifti1Image(t_values, img.affine)
nib.save(img_t, 't_values_map.nii')

# binary mask for each threshold
img_mask1 = nib.Nifti1Image(mask1, img.affine)
nib.save(img_mask1, 'mask_05.nii')

img_mask2 = nib.Nifti1Image(mask2, img.affine)
nib.save(img_mask2, 'mask_01.nii')

img_mask3 = nib.Nifti1Image(mask3, img.affine)
nib.save(img_mask3, 'mask_001.nii')
  
