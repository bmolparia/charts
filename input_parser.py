from tree import Node, Tree

def main(fpath):

    fhand = open(fpath,'r')
    header = fhand.readline()
    rankInd,nameInd,totalInd,samples = parse_header(header)

    Data = {}
    for i in samples:
        Data[i] = {}

    dataline = fhand.readline()

    while dataline:
        rankID,name,total,taxlvl,sample_values =
            parse_line(dataline,rankInd,nameInd,totalInd,samples)



        dataline = fhand.readline()

    fhand.close()
    return Data

def hierarchy(rank):

    rank = rank.split('.')
    i = 0
    while i < len(rank):
        yield ('.').join(rank[0:i+1])
        i+= 1

def parse_line(,line,rankInd,nameInd,totalInd,samples):

    line = line.replace('\n','').split('\t')

    rankID = line[rankInd]
    name  = line[nameInd]
    total  = int(line[totalInd])
    taxlvl = rankID.count('.')

    sample_values = {}
    for i in samples:
        sample_values[i] = int(line[samples[i]])

    return rankID,name,total,taxlvl,sample_values


def parse_header(line):
    ''' This function reads the header and stores the location of each column
    Column header example - level rank  name  total  sample1 sample2...'''

    line = line.replace(' ','').replace('\n','').split('\t')

    rankInd  = line.index('rank')
    nameInd  = line.index('name')
    totalInd = line.index('total')

    samples = {}
    for i in line[totalInd+1:]:
        if i != '':
            samples[i]  = line.index(i)

    return rankInd,nameInd,totalInd,samples


if __name__ == "__main__":

    fpath = './tests/test.tsv'
    t = taxParser(fpath)
    d =  t.main()
    for i in d:
        print i,'\t',d[i]
