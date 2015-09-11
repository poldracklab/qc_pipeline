# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:54:07 2015

@author: craigmoodie
"""

import sys
sys.path.insert(0, '/home/cmoodie/qc_pipeline')

from nipype.pipeline.engine import Workflow, Node, MapNode, JoinNode

from variables import data_dir, work_dir, subject_list, plugin, plugin_args

import gc
import pylab as plt
import nibabel as nb
from matplotlib.backends.backend_pdf import PdfPages
from qap import calc_mean_func, load_mask, load_func, calc_dvars, mean_outlier_timepoints, mean_quality_timepoints, fd_jenkinson, summarize_fd, median_tsnr

qap_workflow = Workflow(name="qap_workflow")

qap_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(epi="*_{subject_id}_*/rfMRI_REST_{pe_dir}_BIC_v2/*_00001.nii*",AFNI_motion="/share/PI/russpold/workdir/Afni_volreg_workflow/_pe_dir_{pe_dir}_subject_id_{subject_id}/Afni_Motion_Correction/mapflow/_Afni_Motion_Correction0/*_00001.aff12.1D")
file_list = Node(SelectFiles(templates), name = "EPI_and_Afni_Motion_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list), ("pe_dir", ["LR", "RL"])]


from nipype.interfaces.fsl import BET

mask_gen = MapNode(BET(), name="Mask_Generation", iterfield="in_file")
mask_gen.inputs.mask = True
mask_gen.inputs.out_file = "bet_mean"



from qap_metrics import qap_report
from report_generate import generate_report
from nipype.interfaces.utility import Function



qap_metrics_node = MapNode(Function(input_names=["func_file","func_mask","motion_matrix_file"],
                                 output_names=["func_dvars", "func_outlier", "func_quality", "mtsnr", "mean_fd", "num_fd", "perc_fd"],
                                 function=qap_report), name="QAP_Metrics_Generation", iterfield=["func_file","func_mask","motion_matrix_file"])


#report_node = Node(Function(input_names=["first_plot", "second_plot", "third_plot", "fourth_plot"],
#                            output_names=["report_file"],
#                            function=generate_report), name="QAP_Report", iterfield=["epi", "AFNI_motion"])
#report_node.inputs.output_file = "report_qap.pdf"
        


qap_workflow.connect(file_list, "epi", mask_gen, "in_file")

qap_workflow.connect(file_list, "epi", qap_metrics_node, "func_file")
qap_workflow.connect(mask_gen, "out_file", qap_metrics_node, "func_mask")
qap_workflow.connect(file_list, "AFNI_motion", qap_metrics_node, "motion_matrix_file")



#qap_workflow.connect(qap_metrics_node, "func_dvars", report_node, "first_plot")
#qap_workflow.connect(qap_metrics_node, "func_outlier", report_node, "second_plot")
#qap_workflow.connect(qap_metrics_node, "func_quality", report_node, "third_plot")
#qap_workflow.connect(qap_metrics_node, "mtsnr", report_node, "fourth_plot")

qap_workflow.run()
#qap_workflow.run(plugin=plugin, plugin_args=plugin_args)



#from nipype.interfaces.utility import Function 
   
#qap_metrics = Function(input_names=["func_file","func_mask","motion_matrix_file"],
                            #output_names=["func_dvars", "func_outlier", "func_quality", "mtsnr", "mean_fd", "num_fd", "perc_fd"],
                            #function=qap_report)  
    
#qap_metrics(func_file="S0799AAW_P126317_6_7_00001.nii.gz",func_mask_file = "mean_mask.nii.gz",motion_matrix_file="S0799AAW_P126317_6_7_00001.aff12.1D")



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