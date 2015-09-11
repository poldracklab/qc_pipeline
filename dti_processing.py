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

dti_workflow = Workflow(name="dti_workflow")

dti_workflow.base_dir = work_dir
dti_workflow.base_dir = "/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/test_output/"

from nipype import SelectFiles
templates = dict(dwi="*_{subject_id}_*/DWI_{direct_dir}_{pe_dir}/*_00001.nii*")
templates = dict(dwi1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/S1543TWL_P126317_1_30_00001.nii")#,
                 bval1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/s030a001.bval",
                 bvec1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/s030a001.bvec",
                 dwi2="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/S1543TWL_P126317_1_28_00001.nii",
                 bval1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_RL/s028a001.bval",
                 bvec1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_Rl/s028a001.bvec")
file_list = Node(SelectFiles(templates), name = "DWI_File_Selection")
#file_list.inputs.base_directory = data_dir
file_list.inputs.base_directory = "/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/NIDB-171/20150317_124055_S9905QEN3/15/"
file_list.iterables = [("subject_id", subject_list), ("direct_dir", ["dir90", "dir91"]) ("pe_dir", ["LR", "RL"])]

dwi1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/S1543TWL_P126317_1_30_00001.nii"
bval1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/s030a001.bval"
bvec1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/s030a001.bvec"
dwi2="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_LR/S1543TWL_P126317_1_28_00001.nii"
bval1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_RL/s028a001.bval"
bvec1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir91_Rl/s028a001.bvec"


from nipype.interfaces.fsl import TOPUP
#topup = MapNode(TOPUP(), name="TopUp", iterfield="in_file")
topup = TOPUP()
topup.inputs.in_file = "/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/DWI_dir90_SBRef_merged.nii.gz"
topup.inputs.encoding_file = "/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/dti/Subj1_DWI_Acq_Params.txt"
topup.inputs.output_type = "NIFTI_GZ"
topup.run()


from nipype.interfaces.fsl import SigLoss
sigloss = SigLoss()
sigloss.inputs.in_file = "phase.nii"
sigloss.inputs.echo_time = 0.03
sigloss.inputs.output_type = "NIFTI_GZ"
sigloss.run()


#
#
from nipype.interfaces.fsl import Eddy
eddy = Eddy()
eddy.inputs.in_file = dwi
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

dti_workflow.connect(file_list, "dti", topup, "in_file")
dti_workflow.connect(file_list, "dti", SigLoss, "in_file")
dti_workflow.connect(file_list, "dti", Eddy, "in_file")
dti_workflow.connect(file_list, "dti", cmon, "in_file")

dti_workflow.run(plugin=plugin, plugin_args=plugin_args)
dti_workflow.run()