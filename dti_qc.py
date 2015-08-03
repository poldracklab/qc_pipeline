# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 17:50:13 2015

@author: craigmoodie
"""


from nipype.pipeline.engine import Workflow, Node, MapNode
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.camino as camino
import nipype.interfaces.fsl as fsl
import nipype.interfaces.camino2trackvis as cam2trk
import nipype.algorithms.misc as misc
import os                                    # system functions

from variables import data_dir, work_dir, subject_list, plugin, plugin_args

dti_workflow = Workflow(name="qc_workflow")

dti_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(dti="*_{subject_id}_*/DWI_{direct_dir}_{pe_dir}/*_00001.nii*")
file_list = Node(SelectFiles(templates), name = "DWI_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list), ("direct_dir", ["dir90", "dir91"]) ("pe_dir", ["LR", "RL"])]


from nipype.interfaces.fsl import TOPUP
topup = TOPUP()
topup.inputs.in_file = "b0_b0rev.nii"
topup.inputs.encoding_file = "topup_encoding.txt"
topup.inputs.output_type = "NIFTI_GZ"


from nipype.interfaces.fsl import SigLoss
sigloss = SigLoss()
sigloss.inputs.in_file = "phase.nii"
sigloss.inputs.echo_time = 0.03
sigloss.inputs.output_type = "NIFTI_GZ"


from nipype.interfaces.fsl import Eddy
eddy = Eddy()
eddy.inputs.in_file = 'dti.nii'
eddy.inputs.in_mask  = 'epi_mask.nii'
eddy.inputs.in_index = 'epi_index.txt'
eddy.inputs.in_acqp  = 'epi_acqp.txt'
eddy.inputs.in_bvec  = 'bvecs.scheme'
eddy.inputs.in_bval  = 'bvals.scheme'


import nipype.interfaces.camino as cmon
fit = cmon.DTIFit()
fit.inputs.scheme_file = 'A.scheme'
fit.inputs.in_file = 'tensor_fitted_data.Bdouble'
fit.run()     

dti_workflow.connect(file_list, "dti", TOPUP, "in_file")
dti_workflow.connect(file_list, "dti", SigLoss, "in_file")
dti_workflow.connect(file_list, "dti", Eddy, "in_file")
dti_workflow.connect(file_list, "dti", cmon, "in_file")

dti_workflow.run(plugin=plugin, plugin_args=plugin_args)