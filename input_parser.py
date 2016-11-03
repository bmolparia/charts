from tree import Node, Tree

def main(fpath):

    fhand = open(fpath,'r')
    header = fhand.readline()
    rankInd,nameInd,totalInd,samples = parse_header(header)

    ## Create a dictionary which has every sample as a key. The value will be a
    ## tree data structure and add the root info, the second line is expected
    ## to contain the information of the root node.
    Data = {}
    root_info = fhand.readline()
    rankID,name,total,taxlvl,sample_values = parse_line(root_info,rankInd,
                                                    nameInd,totalInd,samples)

    for sample_name in samples:
        Data[sample_name] = Tree(name=sample_name)
        root_node = Node(name='{}:root'.format(sample_name),
                         count=sample_values[sample_name],level=[0])
        Data[sample_name].root = root_node

    ## Add rest of the information
    dataline = fhand.readline()
    while dataline:
        rankID,name,total,taxlvl,sample_values = parse_line(dataline,rankInd,
                                                       nameInd,totalInd,samples)

        depth = taxlvl
        level = rankID.split('.')
        for samp in samples:
            tree = Data[samp]
            count = sample_values[samp]
            sampInd = samples[samp]

            samp_node = Node(name=name,level=level,count=count)
            tree.add_node(samp_node,level)

        dataline = fhand.readline()

    fhand.close()
    return Data

def hierarchy(rank):

    rank = rank.split('.')
    i = 0
    while i < len(rank):
        yield ('.').join(rank[0:i+1])
        i+= 1

def parse_line(line,rankInd,nameInd,totalInd,sampleInds):

    line = line.replace('\n','').split('\t')

    rankID = line[rankInd]
    name  = line[nameInd]
    total  = int(line[totalInd])
    taxlvl = rankID.count('.')  ## This is the depth of the node

    sample_values = {}
    for i in sampleInds:
        sample_values[i] = int(line[sampleInds[i]])

    return rankID,name,total,taxlvl,sample_values


def parse_header(line):
    ''' This function reads the header and stores the location of each column
    Column header example - level rank  name  total  sample1 sample2...'''

    line = line.replace(' ','').replace('\n','').split('\t')

    rankInd  = line.index('rankID')
    nameInd  = line.index('taxon')
    totalInd = line.index('total')

    samples = {}
    for i in line[totalInd+1:]:
        if i != '':
            samples[i]  = line.index(i)

    return rankInd,nameInd,totalInd,samples


if __name__ == "__main__":

    fpath = './tests/test.tsv'
    d =  main(fpath)
    for i in d:
        print(i,'\t',d[i],d[i].root, d[i].find_node_by_level(['0','2','7','4','1','18','2']))
