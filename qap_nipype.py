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

from qap_metrics import qap_report
from report_generate import generate_report

qap_metrics_node = JoinNode(Function(input_names=["func_file","func_mask","motion_matrix_file","output_file"],
                            output_names=["func_dvars", "func_outlier", "func_quality", "mtsnr"],
                            function=qap_report), name="QAP_Metrics_Generation", iterfield=["epi", "realignment_parameters_file"])
qap_metrics_node.inputs.output_file = "report.pdf"


report_node = MapNode(Function(input_names=["output_file", "first_plot", "second_plot", "third_plot", "fourth_plot"],
                            output_names=["report_file"],
                            function=generate_report), name="QAP_Report", iterfield=["epi", "realignment_parameters_file"])
report_node.inputs.output_file = "report.pdf"

qap_workflow.connect(file_list, "epi", qap_metrics_node, "func_file")
qap_workflow.connect(file_list, "epi", qap_metrics_node, "func_mask")
qap_workflow.connect(qap_metrics_node, "func_dvars", report_node, "first_plot")
qap_workflow.connect(qap_metrics_node, "func_outlier", report_node, "second_plot")
qap_workflow.connect(qap_metrics_node, "func_quality", report_node, "third_plot")
qap_workflow.connect(qap_metrics_node, "mtsnr", report_node, "fourth_plot")

qap_workflow.run(plugin=plugin, plugin_args=plugin_args)