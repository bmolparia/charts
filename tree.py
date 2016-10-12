import random.random as random

class Node(object):

    def __init__(self):
        self.name = None
        self.counts = None
        self._parent = None
        self._child = None

    def __str__(self):
        return '{}:{}'.format(self.name,self.counts)

    @property
    def child(self):
        ''' Defines the child attribute of a node. This should be a list of
        Node objects.'''
        return self._child

    @property
    def parent(self):
        ''' Defines the parent attribute of a node. This should be a Node
        object.'''
        return self._parent

    @child.setter
    def child(self,value):
        ''' Defines the set attribute function to set a child.'''
        try:
            assert all([isinstance(x, Node) for x in value])
        except AssertionError:
            raise TypeError('The child attribute should be a list of Node  \
            objects')
        self._child = value

    @parent.setter
    def parent(self,value):
        ''' Defines the set attribute function to set a parent.'''
        try:
            assert isinstance(value, Node)
        except AssertionError:
            raise TypeError('A parent has to be another Node object')
        self._parent = value

    def add_child(self,value):
        ''' This function adds a child to the list of children for this Node. It
        will create a list if one doesn't exist.'''
        try:
            assert isinstance(value,Node)
        except AssertionError:
            raise TypeError('A child should be a Node object')
        if self.child == None:
            self.child = [value]
        else:
            self.child.append(value)


class Tree(object):

    def __init__(self,name=None):
        self.levels = None
        self._root = None
        self.name = name


    @property
    def root(self):
        ''' Defines the root of the tree. This should be a Node onject with the
        parent set as None.'''
        return self._root

    @root.setter
    def root(self,value):
        ''' Defines the set attribute function to set a root for the tree.'''
        try:
            assert isinstance(value, Node)
            assert (value.parent == None)
        except AssertionError:
            raise TypeError('The root of the tree has to be a Node object with \
            the parent set to None.')
        self._root = value
