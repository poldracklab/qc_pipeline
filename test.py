# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from nipype import SelectFiles
#templates = dict(T1="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/{subject_id}/T1w_MPR_BIC_v1/*00001.nii*",
#                 epi="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/{subject_id}/rfMRI_REST_RL_BIC_v2/*00001.nii.gz")
#sf = SelectFiles(templates)
#
#print "%s" %(T1) 

from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.fsl import MCFLIRT

from variables import data_dir, work_dir, subject_list, plugin

import gc
import pylab as plt
import nibabel as nb
from matplotlib.backends.backend_pdf import PdfPages
from mriqc.volumes import plot_mosaic, plot_distrbution_of_values
from mriqc.motion import plot_frame_displacement

test_workflow = Workflow(name="qc_workflow")

test_workflow.base_dir = work_dir


from nipype import SelectFiles
templates = dict(T1="*_{subject_id}_*/T1w_MPR_BIC_v1/*00001.nii*", 
                 epi="*_{subject_id}_*/rfMRI_REST_{p_dir}_BIC_v2/*_00001.nii*")
file_list = Node(SelectFiles(templates), name = "EPI_and_T1_File_Selection")
file_list.inputs.base_directory = data_dir
file_list.iterables = [("subject_id", subject_list), ("p_dir", ["LR", "RL"])]
#file_list.id = "6"
#file_results = sf.run()
#file_results.outputs




motion_correct = MapNode(MCFLIRT(), name="Motion_Correction", iterfield="in_file")
motion_correct.inputs.output_type = "NIFTI_GZ"
motion_correct.inputs.save_plots=True

#mcflt = MCFLIRT(in_file="/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/rfMRI_REST_RL_BIC_v2/S1543TWL_P126317_1_8_00001.nii", cost='mutualinfo',save_rms=True)
#mcflt.out_file="S1543TWL_P126317_1_8_00001"
#mcflt.par_file="S1543TWL_P126317_1_8_00001"
#mcflt.rms_files="S1543TWL_P126317_1_8_00001"
#mcflt.mean_img="S1543TWL_P126317_1_8_00001_mean"
#mcflt_out = mcflt.run()



def report_func2(epi,realignment_parameters_file,output_file):
    
    import gc, os
    import pylab as plt
    import nibabel as nb
    from matplotlib.backends.backend_pdf import PdfPages
    from mriqc.volumes import plot_mosaic, plot_distrbution_of_values
    from mriqc.motion import plot_frame_displacement

    report = PdfPages(output_file)

    epi_nii = nb.load(epi) 
    mean_epi = epi_nii.get_data().mean(axis=3)

    fig = plot_mosaic(mean_epi, title="Mean EPI node output", figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)    
    fig.clf()

    epi_std = epi_nii.get_data().std(axis=3)
    epi_tsnr = mean_epi/epi_std
    fig = plot_mosaic(epi_tsnr, title="tSNR node output", figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)
    fig.clf()

    fig = plot_frame_displacement(realignment_parameters_file, figsize=(8.3, 8.3))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    report.close()
    gc.collect()
    plt.close()
    return os.path.abspath(output_file)
    

#return report


from nipype.interfaces.utility import Function
                             
 
#report_func_interface.inputs.epi_nii = nb.load("/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/rfMRI_REST_RL_BIC_v2/S1543TWL_P126317_1_8_00001.nii")
#report_func_interface.inputs.output_file="test_report"
#rep_run = report_func_interface.run()


report_node = MapNode(Function(input_names=["epi","realignment_parameters_file","output_file"],
                            output_names=["report_file"],
                            function=report_func2), name="QC_Report", iterfield=["epi", "realignment_parameters_file"])
#report_node.inputs.epi_nii = nb.load("/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/10_Subject_ICA_test/Subject_1/rfMRI_REST_RL_BIC_v2/S1543TWL_P126317_1_8_00001.nii")
report_node.inputs.output_file = "report.pdf"

 
test_workflow.connect(file_list, "epi", motion_correct, "in_file")
test_workflow.connect(motion_correct, "par_file", report_node, "realignment_parameters_file")
test_workflow.connect(file_list, "epi", report_node, "epi")

test_workflow.run(plugin=plugin)