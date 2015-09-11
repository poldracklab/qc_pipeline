# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:50:29 2015

@author: craigmoodie
"""

from nipype.pipeline.engine import Workflow, Node, MapNode

from variables import data_dir, work_dir, subject_list, plugin, plugin_args

from qap import anatomical_reorient_workflow, run_anatomical_reorient, anatomical_skullstrip_workflow, run_anatomical_skullstrip, flirt_anatomical_linear_registration, run_flirt_anatomical_linear_registration, ants_anatomical_linear_registration, run_ants_anatomical_linear_registration, segmentation_workflow, 


run_anatomical_reorient()


run_anatomical_skullstrip()


run_flirt_anatomical_linear_registration()


run_ants_anatomical_linear_registration()


run_segmentation_workflow()