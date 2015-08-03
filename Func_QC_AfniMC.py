# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.fsl import MCFLIRT

from variables_AFNI import data_dir, work_dir, subject_list, plugin, plugin_args

import nibabel as nb



Afni_workflow = Workflow(name="Afni_volreg_workflow")

Afni_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(epi="*_{subject_id}_*/rfMRI_REST_{pe_dir}_BIC_v2/*_00001.nii*")
file_list = Node(SelectFiles(templates), name = "EPI_and_T1_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list), ("pe_dir", ["LR", "RL"])]



from nipype.interfaces.afni import Volreg
volreg_motion = MapNode(Volreg(), name="Afni_Motion_Correction", iterfield="in_file")
volreg_motion.inputs.args = '-Fourier -twopass'
volreg_motion.inputs.zpad = 1
#volreg_motion.inputs.basefile = "in_file"
volreg_motion.inputs.outputtype = "NIFTI_GZ"
volreg_motion.inputs.verbose = True
volreg_motion.inputs.out_file = "afni_test"
volreg_motion.inputs.oned_file = "S0799AAW_P126317_6_7_00001"
volreg_motion.inputs.oned_matrix_save = "S0799AAW_P126317_6_7_00001"



####### AFNI input that worked #########
## 3dvolreg -verbose -zpad 1 -dfile test_params -1Dfile test_motion_file -1Dmatrix_save test_motion_transf_mat -prefix test -heptic -base S0799AAW_P126317_6_7_00001.nii.gz[0] S0799AAW_P126317_6_7_00001.nii.gz

#
#from nipype.interfaces.utility import Function
#                             
 
#report_func_interface.inputs.epi_nii = nb.load("/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/rfMRI_REST_RL_BIC_v2/S1543TWL_P126317_1_8_00001.nii")
#report_func_interface.inputs.output_file="test_report"
#rep_run = report_func_interface.run()

#
#report_node = MapNode(Function(input_names=["epi","realignment_parameters_file","output_file"],
#                            output_names=["report_file"],
#                            function=report_func2), name="QC_Report"])#, iterfield=["epi", "realignment_parameters_file"])
##report_node.inputs.epi_nii = nb.load("/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/rfMRI_REST_RL_BIC_v2/S1543TWL_P126317_1_8_00001.nii")
#report_node.inputs.output_file = "report.pdf"

 
Afni_workflow.connect(file_list, "epi", volreg_motion, "in_file")
#Afni_workflow.run()
Afni_workflow.run(plugin=plugin, plugin_args=plugin_args)