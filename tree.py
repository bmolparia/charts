class Node(object):

    def __init__(self,name=None,count=None,level=None):
        self.name = name
        self.count = count
        self.level = level
        self._parent = None
        self._child = None

    def __str__(self):
        return 'Node({}:{}:{})'.format(self.name,self.count,self.level)

    @property
    def child(self):
        ''' Defines the child attribute of a node. This should be a list of
        Node objects. '''
        return self._child

    @property
    def parent(self):
        ''' Defines the parent attribute of a node. This should be a Node
        object. '''
        return self._parent

    @child.setter
    def child(self,value):
        ''' Defines the set attribute function to set a child. '''
        try:
            assert all([isinstance(x, Node) for x in value])
        except AssertionError:
            raise TypeError('The child attribute should be a list of Node  \
            objects')
        self._child = value

    @parent.setter
    def parent(self,value):
        ''' Defines the set attribute function to set a parent. '''
        try:
            assert isinstance(value, Node)
        except AssertionError:
            raise TypeError('A parent has to be another Node object')
        self._parent = value

    def add_child(self,value):
        ''' This function adds a child to the list of children for this Node. It
        will create a list if one doesn't exist. '''
        try:
            assert isinstance(value,Node)
        except AssertionError:
            raise TypeError('A child should be a Node object')
        if self.child == None:
            self.child = [value]
        else:
            self.child.append(value)

        return value

class Tree(object):

    def __init__(self,name=None):
        self.levels = None
        self._root = None
        self.name = name

    @property
    def root(self):
        ''' Defines the root of the tree. This should be a Node onject with the
        parent set as None. '''
        return self._root

    @root.setter
    def root(self,value):
        ''' Defines the set attribute function to set a root for the tree. '''
        try:
            assert isinstance(value, Node)
            assert (value.parent == None)
        except AssertionError:
            raise TypeError('The root of the tree has to be a Node object with \
            the parent set to None.')
        self._root = value

    def find_node_by_level(self,inp_level):
        ''' Returns a node given a level. Returns None if a node isn't found.'''

        depth = 1
        max_depth = len(inp_level)
        starting_node = self._root

        while depth < max_depth:
            next_node = None
            if starting_node.child == None:
                pass
            else:
                for n in starting_node.child:
                    if n.level == inp_level[0:depth+1]:
                        next_node = n
                        depth += 1
                        starting_node = next_node
            if next_node == None:
                break

        return next_node

    def add_node(self,node,inp_level):
        ''' Adds a node at the specified level. This fucntion will attempt to
        create the parent nodes if they don't exist. Parents will be just blank
        nodes. '''

        try:
            assert isinstance(node, Node)
        except AssertionError:
            raise TypeError('Input node has to be a Node object')

        depth = 1
        max_depth = len(inp_level)
        starting_node = self._root

        while depth < (max_depth-1):
            current_level = inp_level[0:depth+1]
            current_node = self.find_node_by_level(current_level)
            if isinstance(current_node, Node):
                # If node exists, do nothing
                starting_node = current_node
                depth+=1
            else:
                # If node doesn't exist, add it
                starting_node = starting_node.add_child(Node(level=
                                                                current_level))
                depth+=1
        # When the required depth is reached, add the node provided as Input
        starting_node.add_child(node)

        return node

    def _rec_search(self,curr_depth,final_depth,node):
        ''' This function returns a list of nodes at a given depth from the node
        provided as the input. '''

        if curr_depth == final_depth:
            return [node]
        else:
            ans = []
            for new_node in node.child:
                ans += self._rec_search(curr_depth+1,final_depth,new_node)
            return ans

    def get_nodes_by_depth(self,depth):
        ''' This function returns a list of node attributes at a given depth
        starting from the root. '''

        return self._rec_search(0,depth,self.root)
