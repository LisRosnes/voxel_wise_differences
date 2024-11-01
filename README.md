# voxel_wise_differences

Given .nii images of two groups of patients, the code will calcuate voxel-wise differences between the two groups using a t-test. The code thresholds the output at various p_values to generate masks. 

Uses nibabel, numpy, os

Change the name of the files in variables "group1_files" and "group2_files" to the .nii images being compared

You can download and use MRIcron to visualize differences 
