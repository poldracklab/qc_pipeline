# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 18:30:42 2015

@author: craigmoodie
"""

#from nipype.pipeline.engine import Workflow, Node, MapNode
#
#from variables import data_dir, work_dir, subject_list, plugin, plugin_args
#
#import gc
#import pylab as plt
#import nibabel as nb
#from matplotlib.backends.backend_pdf import PdfPages
#from mriqc.volumes import plot_mosaic, plot_distrbution_of_values
#from mriqc.motion import plot_frame_displacement
#
#test_workflow = Workflow(name="qc_workflow")
#
#test_workflow.base_dir = work_dir


#from nipype import SelectFiles
#templates = dict(T1="*_{subject_id}_*/T1w_MPR_BIC_v1/*00001.nii*")
#file_list = Node(SelectFiles(templates), name = "EPI_and_T1_File_Selection")
#file_list.inputs.base_directory = data_dir
#file_list.iterables = [("subject_id", subject_list), ("p_dir", ["LR", "RL"])]


from nipype.interfaces.fsl import BET

mask_gen = BET()
mask_gen.inputs.in_file = "/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/T1w_MPR_BIC_v1/S1543TWL_P126317_1_19_00001.nii"
mask_gen.inputs.mask = True
mask_gen.inputs.out_file = "bet_mean"
mask_gen.run()


#mask_gen = MapNode(BET(), name="Mask_Generation", iterfield="in_file")



#from spatial_qc import summary_mask, ghost_all, ghost_direction, ghost_mask, fwhm, artifacts, efc, cnr, snr
#
#
#summary_mask()