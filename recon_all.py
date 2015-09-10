# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:39:05 2015

@author: craigmoodie
"""

from nipype.pipeline.engine import Workflow, Node, MapNode
from variables import data_dir, work_dir, subject_list, plugin, plugin_args


surface_workflow = Workflow(name="qc_workflow")

surface_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(T1="*_{subject_id}_*/T1w_MPR_BIC_v1/*00001.nii*")
file_list = Node(SelectFiles(templates), name = "EPI_and_T1_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list)]


from nipype.interfaces.freesurfer import ReconAll
reconall = Node(ReconAll(), name = "Recon_All")
reconall.inputs.subject_id = "subject_id"
reconall.inputs.directive = 'all'
reconall.inputs.subjects_dir = data_dir
#reconall.inputs.T1_files = "T1"
#reconall.run()

surface_workflow.connect(file_list,"T1", reconall, "T1_files")
surface_workflow.run(plugin=plugin, plugin_args=plugin_args)