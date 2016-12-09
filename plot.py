import argparse

import input_parser
from multi_level_pi import plot as ml_plot

def sb_plot():
    pass

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
    parser.add_argument('-d', metavar="Depth", dest = 'depth_s', default=1,
    				help='The level/depth to begin plotting from',type=int)
    parser.add_argument('-m', metavar="MaxDepth", dest = 'maxdepth', default=3,
    			    help='The level/depth at which the plot ends',type=int)

    args = parser.parse_args()
    data = input_parser.main(args.inp)

    plot = plot_functions[args.type]
    plot(data,args.out,args.depth_s,args.maxdepth)
