class Node(object):

    def __init__(self):
        self.name = None
        self.counts = None
        self._parent = None
        self._child = None

    def __str__(self):
        return '{}.{}'.format(self.name,self.counts)

    @property
    def child(self):
        return self._child

    @property
    def parent(self):
        return self._parent

    @child.setter
    def child(self,value):
        try:
            assert all([isinstance(x, Node) for x in value])
        except AssertionError:
            raise TypeError('A child object should be a list of Node objects')
        self._child = value

    @parent.setter
    def parent(self,value):
        try:
            assert isinstance(value, Node)
        except AssertionError:
            raise TypeError('A parent has to be another Node object')
        self._parent = value


class Tree(object):

    def __init__(self):
        self.leaf = None
