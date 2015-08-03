# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:54:08 2015

@author: craigmoodie
"""
def generate_report(output_file, first_plot, second_plot, third_plot, fourth_plot):
    
    import os
    import pylab as plt
    import nibabel as nb
    from matplotlib.gridspec import GridSpec
    from matplotlib.backends.backend_pdf import PdfPages

    report = PdfPages(output_file)

    fig = plt.figure()

    grid = GridSpec(2,2)

    ax = plt.subplot(grid[0,0])
    ax2 = plt.subplot(grid[1,0])
    ax3 = plt.subplot(grid[0,1])
    ax4 = plt.subplot(grid[1,1])

    ax.plot(first_plot)  
    ax2.plot(second_plot)
    ax3.plot(third_plot)
    ax4.plot(fourth_plot)

    ax.set_xlim((0, len(first_plot)))
    ax.set_ylabel("Random Distribution 1")
    ax.set_xlabel("Index 1")
    ax.set_title('ax1 title')
    ylim = ax.get_ylim()

    ax2.set_xlim((0, len(second_plot)))
    ax2.set_ylabel("Random Distribution 2")
    ax2.set_xlabel("Index 2")
    ax2.set_title('ax2 title')
    ylim = ax2.get_ylim()

    ax3.set_xlim((0, len(third_plot)))
    ax3.set_ylabel("Random Distribution 3")
    ax3.set_xlabel("Index 3")
    ax3.set_title('ax3 title')
    ylim = ax3.get_ylim()

    ax4.set_xlim((0, len(fourth_plot)))
    ax4.set_ylabel("Random Distribution 4")
    ax4.set_xlabel("Index 4")
    ax4.set_title('ax4 title')
    ylim = ax4.get_ylim()

    fig.subplots_adjust(wspace=.5, hspace=.5)

    report.savefig(fig, dpi=300)
    report.close()
    
    return os.path.abspath(output_file)
    
#generate_report(output_file="report_generated.pdf", first_plot=test_nums, second_plot=test_nums1, third_plot=test_nums2, fourth_plot=test_nums3)