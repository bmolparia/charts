import argparse

import input_parser
from multi_level_pi import plot as ml_plot
from stacked_bar import plot as sb_plot

def parse_sample_sheet(filepath):
	fin  = open(filepath,'r')
	data = fin.readlines()
	fin.close()

	snames = []
	sdict  = {}
	for line in data:
		line = line.replace('\n','').split('\t')
		sdict[line[0]] = line[1]
		snames.append(line[0])

	return snames,sdict

if __name__ == "__main__":

    plot_functions = {'multi_pi':ml_plot,'stacked_bar':sb_plot}

    parser = argparse.ArgumentParser(description='This script can be used to \
    plot tree data in different styles. It takes an input file in the \
    format produced by the software "mothur". The default chart plotted will be\
    at level 3. Multiple level charts will start at root and end after 3 \
    as default behavior. This can be changed using the optional parameters.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inp', metavar='Input',
    				help='path to the input file')
    parser.add_argument('out', metavar='Output',
    				help='path for the output image')
    parser.add_argument('-t', metavar='Plot Type', dest='type',
                    help='The kind of chart you want to plot. Allowed values \
                    are: '+(', ').join(list(plot_functions)),
                    choices=list(plot_functions), required=True )
    parser.add_argument('-s', metavar='Sample Sheet', dest='ssheet',
                    help='TSV file contatining mappings of sample names to \
                    sample ids.', default=None)
    parser.add_argument('-d', metavar="Depth", dest = 'depth', default=1,
    				help='The level/depth to begin plotting from',type=int)
    parser.add_argument('-m', metavar="MaxDepth", dest = 'maxdepth', default=3,
    			    help='The level/depth at which the plot ends',type=int)

    args = parser.parse_args()
    data,sample_ids = input_parser.main(args.inp)
    if args.ssheet == None:
        sample_names = sample_ids
        sample_dict = {key:key for key in sample_ids}
    else:
        sample_names, sample_dict = parse_sample_sheet(args.ssheet)

    kwargs = {'depth':args.depth, 'maxdepth':args.maxdepth,
            'sample_names':sample_names, 'sample_dict':sample_dict}

    plot = plot_functions[args.type]
    plot(data,args.out,**kwargs)
