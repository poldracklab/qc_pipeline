#!/bin/bash

root=/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/NIDB-171/20150317_124055_S9905QEN3

echo $root
ls $root

cd $root/mean_FA_JHU_ROIs

for roinum in `seq 1 48` ; do
	
	pwd
	ls ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz
	
   fslmaths /Applications/fsl/fsl/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz -thr ${roinum} -uthr ${roinum} JHU_roi_${roinum}_2mm
   fslmaths JHU_roi_${roinum}_2mm.nii.gz -bin JHU_roi_${roinum}_2mm_mask
   fslmaths JHU_roi_${roinum}_2mm_mask -mas ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz -bin DWI_FA_masked_roi_${roinum}
   padroi=`$FSLDIR/bin/zeropad ${roinum} 3`
   
   echo "ROI" ${roinum}
   echo "FA mean with no padding" > FA_means_no_pad.txt
   echo "ROI" ${roinum} >> FA_means_no_pad.txt
   fslmeants -i DWI_FA_masked_roi_${roinum} >> FA_means_no_pad.txt
   echo fslmeants -i DWI_FA_masked_roi_${roinum}
   
   echo "FA mean with 3 voxel padding"
   fslmeants -i ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz -m JHU_roi_${roinum}_2mm_mask -o meants_roi${padroi}.txt
   echo fslmeants -i ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz
   
   echo "FA mean from fslstats"
   echo "Mean whole brain FA"
   fslstats ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz -M
   echo "FA mean from fslstats" > FA_means_from_fslstats.txt
   fslstats -t ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz -k JHU_roi_${roinum}_2mm_mask
   fslstats -t ../fnirted_JHU_ICBM_FA_2mm_subect1.nii.gz -k JHU_roi_${roinum}_2mm_mask -M >> FA_means_from_fslstats.txt
   
done

paste meants_roi*.txt > allmeants_roi.txt