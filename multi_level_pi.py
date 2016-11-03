'''
NOTE - This script creates a multi level pi chart for a tree dataset. If you
run this directly, it takes in an input file in the format produced by the
software "mothur". The default chart is plotted begins at the first level from
the root and ends after 3 levels. This can be changed using the option parameters
depth and maxdepth.
'''

import math
import argparse

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

import input_parser

def get_next_level_of_nodes(nodes):
	new_nodes = []
	for node in nodes:
		try:
			new_nodes += node.child
		except TypeError:
			pass
	return new_nodes

def plot(data,outname,depth=1,maxdepth=3):
	''' This function will plot a multi level pi chart for the given "data" in a
	tree format. "depth" is the starting level for the pi chart, "maxdepth" is
	the level at which the outermost layer is plotted. "outname" is the filepath
	for the chart. '''

	pdfOut = PdfPages(outname)
	num_samples = len(data)
	sampleNames = list(data)

	plotind = 1
	for name in sampleNames[0:1]:

		sample = data[name]

		fig = plt.figure(figsize=(23,15))
		ax  = fig.add_axes([0,0,(15.0/23.0),1],frameon=True)

		root  = sample.root
		total = root.count

		plt.suptitle(name,fontsize=40,x=(15.0/23.0)/2)
		colormaps = {1:'winter',2:'spectral_r',3:'Set1'}
		lgds = []

		#Get the nodes at "depth" starting from the root
		current_nodes = sample.get_nodes_by_depth(depth)
		print(current_nodes)

		while depth <= maxdepth:

			counts = [x.count for x in current_nodes]
			labels = [x.name for x in current_nodes]

			print(counts,labels)

			cMap      = plt.get_cmap(colormaps[depth])
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
			radi  = 1 - ((maxdepth-depth)*0.3)

			kwargs = dict(startangle=90, colors=colorVals,
						  wedgeprops={'alpha':0.8})
			Pie, text = ax.pie(countsArr, radius = radi, **kwargs)

			legend_entry = fig.legend(Pie,labels ,
			bbox_to_anchor=((15.0/23.0)+((depth-1)*0.15), 1), loc='upper right')

			ax.add_artist(legend_entry)
			plt.setp(Pie,width=width)

			depth += 1
			current_nodes = get_next_level_of_nodes(current_nodes)

		plotind += 1
		#plt.show()

		pdfOut.savefig(fig)
		plt.close()

	pdfOut.close()


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Processes file paths and \
	plotting parameters')
	parser.add_argument('inp', metavar='Input',
						help='path to the input file')
	parser.add_argument('out', metavar='Output',
						help='path for the output image')
	parser.add_argument('-d', metavar="Depth", dest = 'depth', default=1,
						help='The level/depth to begin plotting from')
	parser.add_argument('-m', metavar="MaxDepth", dest = 'maxdepth', default=3,
					help='The level/depth at which the plot ends')

	args = parser.parse_args()
	data = input_parser.main(args.inp)
	plot(data,args.out,args.depth,args.maxdepth)
