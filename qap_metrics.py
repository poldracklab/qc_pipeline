# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 21:23:41 2015

@author: craigmoodie
"""

import sys
sys.path.insert(0, '/home/cmoodie/qc_pipeline')

def qap_report(func_file,func_mask_file,motion_matrix_file):

#    func_file=epi
#    func_mask_file = "mean_mask.nii.gz"
    from qap import calc_mean_func, load_mask, load_func, calc_dvars, mean_outlier_timepoints, mean_quality_timepoints, median_tsnr, summarize_fd

    func_mask = load_mask(func_mask_file)
    func_data = load_func(func_file, func_mask_file)

    func_dvars = calc_dvars(func_data, output_all=True)

    func_outlier = mean_outlier_timepoints(func_file, func_mask_file, out_fraction=True)

    func_quality = mean_quality_timepoints(func_file)

    mtsnr = median_tsnr(func_data)

    mean_fd, num_fd, perc_fd = summarize_fd(motion_matrix_file, threshold=0.2)

    print("FD", mean_fd, "number of TRs outside 0.2 mm", num_fd, "percent of TRs outside 0.2 mm", perc_fd)
    print("DVARS",func_dvars)
    print("Mean of Outliers",func_outlier,"Mean of Quality Timepoints", func_quality, "Median tsnr", mtsnr)
    
    return func_dvars, func_outlier, func_quality, mtsnr, mean_fd, num_fd, perc_fd
    
    
