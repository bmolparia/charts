import math
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def plot(data,outname,sample_names,sample_dict,depth=3,**_):

	# Collect the data
	data_by_taxon = {}
	taxon_name_map = {}
	for sample_name in sample_names:
		sample_id = sample_dict[sample_name]

		sample = data[sample_id]
		root = sample.root
		total = root.count

		current_nodes = sample.get_nodes_by_depth(depth)
		current_nodes = sorted(current_nodes,key = lambda x: x.name)

		for node in current_nodes:
			temp_name = node.name+str(current_nodes.index(node))
			taxon_name_map[temp_name] = node.name
			if temp_name in data_by_taxon:
				data_by_taxon[temp_name].append(node.count/float(total))
			else:
				data_by_taxon[temp_name] = [node.count/float(total)]

	taxon_list = sorted(list(data_by_taxon))
	num_samples = len(sample_names)

	# Setting up the figure
	fig = plt.figure(figsize=(2*num_samples,20))
	ax  = fig.add_subplot(111)
	ax.set_ylim(0,102)

	width = 0.6
	ind = np.arange(len(sample_names))+0.2+(width)
	cMap = plt.get_cmap('Paired')
	cNorm = colors.Normalize(vmin=0, vmax=len(taxon_list))
	sacalar_map = cmx.ScalarMappable(norm=cNorm, cmap=cMap)
	all_bars = []

	# Plotting the figure
	# Initializing
	cindx = 0
	values = np.array(data_by_taxon[taxon_list[0]])*100
	colorVal = sacalar_map.to_rgba(cindx)
	bar = plt.bar(ind, values, width = width, color = colorVal)
	all_bars.append(bar[0])

	# Adding rest of the taxons
	cindx += 1
	for taxon in taxon_list[1:]:
		values2  = np.array(data_by_taxon[taxon])*100
		colorVal = sacalar_map.to_rgba(cindx)

		bar = plt.bar(ind,values2,width = width, bottom = values,
					color = colorVal)
		all_bars.append(bar[0])

		values += values2
		cindx  += 1

	# Labelling
	font = {'family' : 'sans-serif',
	        'weight' : 'bold'}
	mp.rc('font',**font)

	plt.ylabel('Percent',fontsize=35, **font)
	plt.title('Abundance Chart',fontsize=40, x = 0.5, y =1.01, **font)
	plt.xticks(ind, sample_names, fontsize=25,rotation=60, **font)
	plt.yticks(np.arange(0,101,10),fontsize=25, **font)
	legend_names = list(map(lambda x: taxon_name_map[x], taxon_list))
	lgd = plt.legend(all_bars, legend_names, bbox_to_anchor=(1.01, 1), loc=0,
			fontsize=30)
	fig.tight_layout(rect=(0,0,0.85,1))

	plt.savefig(outname,format='png',bbox_extra_artists=(lgd,),bbox_inches='tight')
