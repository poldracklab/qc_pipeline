# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:53:59 2015

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

mask_workflow = Workflow(name="mask_workflow")

mask_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(epi="*_{subject_id}_*/rfMRI_REST_{pe_dir}_BIC_v2/*_00001.nii*",AFNI_motion="/share/PI/russpold/workdir/Afni_volreg_workflow/_pe_dir_{pe_dir}_subject_id_{subject_id}/Afni_Motion_Correction/mapflow/_Afni_Motion_Correction0/*_00001.aff12.1D")
file_list = Node(SelectFiles(templates), name = "EPI_and_Afni_Motion_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list), ("pe_dir", ["LR", "RL"])]


from nipype.interfaces.fsl import BET

mask_gen = MapNode(BET(), name="Mask_Generation", iterfield="in_file")
mask_gen.inputs.mask = True
mask_gen.inputs.out_file = "bet_mean"

mask_workflow.connect(file_list, "epi", mask_gen, "in_file")
mask_workflow.run()