'''
This script creates a multi level pi chart for a tree dataset.
'''

import math

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

def get_next_level_of_nodes(nodes):
    new_nodes = []
    for node in nodes:
        try:
            new_nodes += node.child
        except TypeError:
            pass
    return new_nodes

def plot(data,outname,sample_names,sample_dict,depth=1,maxdepth=3,legend_size=18,**_):
    ''' This function will plot a multi level pi chart for the given "data" in a
    tree format. "depth" is the starting level for the pi chart, "maxdepth" is
    the level at which the outermost layer is plotted. "outname" is the filepath
    for the chart. '''

    pdf_out = PdfPages(outname)

    for sample_name in sample_names:

        sample_id = sample_dict[sample_name]
        sample = data[sample_id]

        num_levels = (maxdepth - depth + 1)
        figure_width = 15+(3.5*num_levels)

        fig = plt.figure(figsize=(figure_width,15))
        ax  = fig.add_axes([0,0,(15.0/figure_width),1],frameon=True)

        root  = sample.root
        total = float(root.count)

        plt.suptitle(sample_name,fontsize=40,x=(15.0/figure_width)/2)
        colormaps = {1:'terrain',2:'nipy_spectral_r',3:'nipy_spectral',4:'rainbow',5:'gist_ncar'}

        #Get the nodes at "depth" starting from the root
        current_depth = depth
        current_nodes = sample.get_nodes_by_depth(current_depth)
        legends = []
        legend_number = 1

        while current_depth <= maxdepth:

            counts = [x.count for x in current_nodes]
            labels = [x.name for x in current_nodes]

            color_map  = plt.get_cmap(colormaps[legend_number%5])
            color_norm = colors.Normalize(vmin=0, vmax=len(counts))
            scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=color_map)

            color_values = scalar_map.to_rgba(range(len(counts)))

            counts_array = np.array(counts)/total
            # Width of the "rings" (percentages if the largest "radius"==1)
            width = 0.75/num_levels
            radi  = 1 - ((maxdepth-current_depth)* (1.0/num_levels))

            kwargs = dict(startangle=90, colors=color_values,
                          wedgeprops={'alpha':1} )
            Pie, text = ax.pie(counts_array, radius=radi, **kwargs)
            plt.setp(Pie,width=width)

            # Add labels to the Wedge objects and sort wedges by angle for
            # legend entries
            Pie_copy = []
            for i in Pie:
                if (i.theta2-i.theta1)>0:
                    index = Pie.index(i)
                    i.label = labels[index]
                    Pie_copy.append(i)

            Pie_copy = sorted(Pie_copy, key=lambda x:(x.theta2-x.theta1),
                              reverse=True)

            xwidth = (1.0/num_levels)*(1-(15.0/figure_width))
            xbeg = (15.0/figure_width)+((legend_number-1) * xwidth)
            ybeg = 0
            height = 1
            ax_legend = fig.add_axes([xbeg,ybeg,width,height],frameon=False)
            ax_legend.xaxis.set_visible(False)
            ax_legend.yaxis.set_visible(False)

            sorted_labels = map(lambda x: x.label, Pie_copy)
            legend_entry = ax_legend.legend(Pie_copy, sorted_labels,
                                                prop={'size':legend_size},
                                                loc='upper left')

            legends.append(legend_entry)
            legend_number += 1

            current_depth += 1
            current_nodes = get_next_level_of_nodes(current_nodes)

        pdf_out.savefig(fig,bbox_inches='tight')
        plt.close()

    pdf_out.close()
