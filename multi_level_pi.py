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

def plot(data,outname,depth=1,maxdepth=3,**_):
	''' This function will plot a multi level pi chart for the given "data" in a
	tree format. "depth" is the starting level for the pi chart, "maxdepth" is
	the level at which the outermost layer is plotted. "outname" is the filepath
	for the chart. '''

	pdfOut = PdfPages(outname)
	num_samples = len(data)
	sampleNames = list(data)

	for name in sampleNames:

		sample = data[name]

		fig = plt.figure(figsize=(23,15))
		ax  = fig.add_axes([0,0,(15.0/23.0),1],frameon=True)

		root  = sample.root
		total = root.count

		plt.suptitle(name,fontsize=40,x=(15.0/23.0)/2)
		colormaps = {1:'winter',2:'spectral_r',3:'Set1'}

		#Get the nodes at "depth" starting from the root
		current_depth = depth
		current_nodes = sample.get_nodes_by_depth(current_depth)

		while current_depth <= maxdepth:
			
			counts = [x.count for x in current_nodes]
			labels = [x.name for x in current_nodes]

			cMap      = plt.get_cmap(colormaps[current_depth])
			cNorm     = colors.Normalize(vmin=0, vmax=len(counts))
			scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cMap)

			colorVals = []
			i = 0
			while i < len(counts):
				colorVals += [scalarMap.to_rgba(i)]
				i += 1

			countsArr = np.array(counts)/total
			# Width of the "rings" (percentages if the largest "radius"==1)
			width = 0.2
			radi  = 1 - ((maxdepth-current_depth)*0.3)

			kwargs = dict(startangle=90, colors=colorVals,
						  wedgeprops={'alpha':0.8})
			Pie, text = ax.pie(countsArr, radius = radi, **kwargs)

			legend_entry = fig.legend(Pie,labels ,
			bbox_to_anchor=((15.0/23.0)+((current_depth-1)*0.15), 1),
							loc='upper right')

			ax.add_artist(legend_entry)
			plt.setp(Pie,width=width)

			current_depth += 1
			current_nodes = get_next_level_of_nodes(current_nodes)

		pdfOut.savefig(fig)
		plt.close()

	pdfOut.close()
