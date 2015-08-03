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

    print("DVARS",func_dvars)
    print("Mean of Outliers",func_outlier,"Mean of Quality Timepoints", func_quality, "Median tsnr", mtsnr)
    
    return func_dvars, func_outlier, func_quality, mtsnr
    
    
qap_report(func_file="S0799AAW_P126317_6_7_00001.nii.gz",func_mask_file = "mean_mask.nii.gz",motion_matrix_file="S0799AAW_P126317_6_7_00001.aff12.1D")



#motion_matrix_file = "test_motion_transf_mat.aff12.1D"
#
#from qap import calc_dvars
#func_dvars = calc_dvars(func_data, output_all=True)
#
#from qap import mean_outlier_timepoints
#func_outlier = mean_outlier_timepoints(func_file, func_mask_file, out_fraction=True)
##
#from qap import mean_quality_timepoints
#func_quality = mean_quality_timepoints(func_file)
##
#print func_outlier
#print func_quality
#
#from qap import fd_jenkinson, summarize_fd
#mean_fd, num_fd, perc_fd = summarize_fd(motion_matrix_file, threshold=0.2)
#
#
#print mean_fd
#print num_fd
#print perc_fd
#
#from qap import median_tsnr
#mtsnr = median_tsnr(func_data)
#print "Median tsnr"
#print mtsnr


#import numpy as np
#func_dvars.save("dvars.txt",func_dvars)
#np.savetxt("dvars.txt",func_dvars,fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
#np.savetxt("outliers.txt",func_outlier,fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
#np.savetxt("quality.txt",func_quality,fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
#np.savetxt("FD.txt",mean_fd,fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
#np.savetxt("median_tsnr.txt",mtsnr,fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')

#import cPickle as pickle
#pickle.dumps(func_dvars,-1)
#pickle.dump(func_dvars, 'dvars_output.txt', pickle.HIGHEST_PROTOCOL)