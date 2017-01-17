'''
This script creates a multi level pi chart for a tree dataset.
'''

import math
import argparse

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

def plot(data,outname,sample_names,sample_dict,depth=1,maxdepth=3,**_):
	''' This function will plot a multi level pi chart for the given "data" in a
	tree format. "depth" is the starting level for the pi chart, "maxdepth" is
	the level at which the outermost layer is plotted. "outname" is the filepath
	for the chart. '''

	pdf_out = PdfPages(outname)

	for sample_name in sample_names:

		sample_id = sample_dict[sample_name]
		sample = data[sample_id]

		num_levels = (maxdepth - depth + 1)
		figure_width = 15+(4*num_levels)

		fig = plt.figure(figsize=(figure_width,15))
		ax  = fig.add_axes([0,0,(15.0/figure_width),1],frameon=True)

		root  = sample.root
		total = root.count

		plt.suptitle(sample_name,fontsize=40,x=(15.0/figure_width)/2)
		colormaps = {1:'spectral_r',2:'Dark2',3:'Set1',4:'Paired'}

		#Get the nodes at "depth" starting from the root
		current_depth = depth
		current_nodes = sample.get_nodes_by_depth(current_depth)
		legends = []
		legend_number = 1

		while current_depth <= maxdepth:

			counts = [x.count for x in current_nodes]
			labels = [x.name for x in current_nodes]

			color_map  = plt.get_cmap(colormaps[legend_number])
			color_norm = colors.Normalize(vmin=0, vmax=len(counts))
			scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=color_map)

			colorVals = []
			i = 0
			while i < len(counts):
				colorVals += [scalar_map.to_rgba(i)]
				i += 1

			countsArr = np.array(counts)/total
			# Width of the "rings" (percentages if the largest "radius"==1)
			width = 0.2
			radi  = 1 - ((maxdepth-current_depth)*0.3)

			kwargs = dict(startangle=90, colors=colorVals,
						  wedgeprops={'alpha':0.8})
			Pie, text = ax.pie(countsArr, radius = radi, **kwargs)

			xwidth = (1.0/num_levels)*(1-(15.0/figure_width))
			xbeg = (15.0/figure_width)+((legend_number-1) * xwidth)
			ybeg = 0
			height = 1
			ax_legend = fig.add_axes([xbeg,ybeg,width,height],frameon=False)
			ax_legend.xaxis.set_visible(False)
			ax_legend.yaxis.set_visible(False)

			legend_entry = ax_legend.legend(Pie, labels, loc='upper left')
			#bbox_to_anchor=(0,1) )

			legends.append(legend_entry)
			legend_number += 1

			plt.setp(Pie,width=width)

			current_depth += 1
			current_nodes = get_next_level_of_nodes(current_nodes)

		pdf_out.savefig(fig)
		plt.close()

	pdf_out.close()
