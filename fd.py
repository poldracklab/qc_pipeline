# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 21:23:41 2015

@author: craigmoodie
"""

import sys
sys.path.insert(0, '/home/cmoodie/qc_pipeline')

def fd_qap(motion_matrix_file):

#    func_file=epi
#    func_mask_file = "mean_mask.nii.gz"
    from qap import summarize_fd

    mean_fd, num_fd, perc_fd = summarize_fd(motion_matrix_file, threshold=0.2)

    print("FD", mean_fd, "number of TRs outside 0.2 mm", num_fd, "percent of TRs outside 0.2 mm", perc_fd)
  
    return mean_fd, num_fd, perc_fd
    
    
fd_qap(motion_matrix_file="S0799AAW_P126317_6_7_00001.aff12.1D")
