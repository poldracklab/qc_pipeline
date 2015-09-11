# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 08:16:51 2015

@author: craigmoodie
"""


from nipype.pipeline.engine import Workflow, Node, MapNode
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine

import sys
sys.path.insert(0, '/home/cmoodie/software/fmriqa')
sys.path.insert(0, '/home/cmoodie/software/dtiqa')


from variables import data_dir, work_dir, subject_list, plugin, plugin_args

dti_qc_workflow = Workflow(name="dti_qc_workflow")

dti_qc_workflow.base_dir = work_dir

from nipype import SelectFiles
templates = dict(dwi="*_{subject_id}_*/DWI_{direct_dir}_{pe_dir}/*_00001.nii*")

dti_qc_reportfunc()

    import dtiqc
    
    dtifile="dwi"
    
    return 
    
    
    