## Installation
git clone https://github.com/bmolparia/charts.git
pip3 install -r requirements.txt

---

## Usage

plot.py [-h] -t Plot Type [-d Depth] [-m MaxDepth] Input Output

This script can be used to plot tree data in different styles. It takes an
input file in the format produced by the software "mothur". The default chart
plotted will be at level 3. Multiple level charts will start at root and end
after 3 as default behavior. This can be changed using the optional
parameters.

### Positional Arguments:
  Input         path to the input file
  Output        path for the output image

### Optional Arguments:
  -h, --help    show this help message and exit
  -t Plot Type  The kind of chart you want to plot. Allowed values are:
                multi_pi, stacked_bar (default: None)
  -d Depth      The level/depth to begin plotting from (default: 1)
  -m MaxDepth   The level/depth at which the plot ends (default: 3)
