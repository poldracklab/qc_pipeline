# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from nipype.interfaces.dcm2nii import Dcm2nii

converter = Dcm2nii()
converter.inputs.source_names = ['/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/20150422_141939_S3543JIU2/1/S3543JIU_2_1_00001_00001_142018317500_142023007000_1755683360.dcm', '/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/20150422_141939_S3543JIU2/1/S3543JIU_2_1_00001_00002_142026262500_142030989000_787790598.dcm','/Users/craigmoodie/Documents/AA_Connectivity_Psychosis/AA_Connectivity_Analysis/20150422_141939_S3543JIU2/1/S3543JIU_2_1_00001_00003_142022290000_142030986000_2249240160.dcm']
converter.inputs.gzip_output = True
converter.inputs.output_dir = '.'

converter.run() 