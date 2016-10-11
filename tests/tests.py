import sure

from ..tree import *

def test_node_str():

    test_node = Node()
    test_node.counts = 23
    test_node.name = 'test'

    str_test = str(test_node)

    str_test.should.be.equal('test.23')
