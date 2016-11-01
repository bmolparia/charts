import sure

from ..tree import *

def test_node_str():
    ''' Tests the str function for the Node object '''
    test_node = Node()
    test_node.count = 23
    test_node.name = 'test'
    test_node.level = [0]

    str_test = str(test_node)

    str_test.should.be.equal('Node(test:23:[0])')

def test_node_add_child():
    ''' Tests the add_child function for the Node object '''

    test_node = Node(level=[0],name='Root')
    lvl_1 = test_node.add_child(Node(level=[0,1],name='0_1'))

    isinstance(lvl_1,Node).should.be.true
    str(lvl_1).should.be.equal('Node(0_1:None:[0, 1])')

def test_tree_find_node_by_level():
    ''' Tests the find_node_by_level function for the Tree object '''

    t = Tree()
    t.root = Node(level=[0],name='Root')

    lvl1_1 = t.root.add_child(Node(level=[0,1],name='0_1'))
    lvl1_2 = t.root.add_child(Node(level=[0,2],name='0_2'))

    lvl1_1_1 = lvl1_1.add_child(Node(level=[0,1,1],name='0_1_1'))
    lvl1_1_2 = lvl1_1.add_child(Node(level=[0,1,2],name='0_1_2'))
    lvl1_1_3 = lvl1_1.add_child(Node(level=[0,1,3],name='0_1_3'))

    lvl1_1_3_1 = lvl1_1_3.add_child(Node(level=[0,1,3,1],name='0_1_3_1'))
    lvl1_1_3_2 = lvl1_1_3.add_child(Node(level=[0,1,3,2],name='0_1_3_2'))

    ans1 = t.find_node_by_level([0,2,3,2])
    ans2 = t.find_node_by_level([0,1,3,2])
    ans3 = t.find_node_by_level([0,2])

    ans1.should.be.equal(None)
    isinstance(ans2,Node).should.be.true
    str(ans2).should.be.equal('Node(0_1_3_2:None:[0, 1, 3, 2])')
    isinstance(ans3,Node).should.be.true
    str(ans3).should.be.equal('Node(0_2:None:[0, 2])')

def test_tree_add_node():
    ''' Tests the add_node function for the Tree object '''

    t = Tree()
    t.root = Node(level=[0],name='Root')

    lvl1_1 = t.root.add_child(Node(level=[0,1],name='0_1'))
    lvl1_2 = t.root.add_child(Node(level=[0,2],name='0_2'))

    n = Node(name='test',level=[0,2,3,2,6],count=23)
    t.add_node(n,[0,2,3,2,6])

    parent2 = t.find_node_by_level([0,2,3])
    parent1 = t.find_node_by_level([0,2,3,2])
    answer = t.find_node_by_level([0,2,3,2,6])

    isinstance(parent2,Node).should.be.true
    isinstance(parent1,Node).should.be.true
    isinstance(answer,Node).should.be.true

    str(parent2).should.be.equal('Node(None:None:[0, 2, 3])')
    str(parent1).should.be.equal('Node(None:None:[0, 2, 3, 2])')
    str(answer).should.be.equal('Node(test:23:[0, 2, 3, 2, 6])')
