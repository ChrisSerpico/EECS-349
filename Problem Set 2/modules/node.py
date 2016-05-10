# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
		'''
		given a single observation, will return the output of the tree
		'''
		
		# if there is no label, split on a decision attribute 
		if (self.label == None):
			# get the attribute that's being split on 
			attribute = instance[self.decision_attribute]
			
			if (self.is_nominal):
				return self.children[attribute].classify(instance)
			else:
				if (attribute < self.splitting_value):
					return self.children[0].classify(instance)
				else:
					return self.children[1].classify(instance)
		# otherwise we're done, and return the label
		else:
			return self.label

    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        nodes = []
        output = ''
        print self.dnf_recurse(nodes, output)[:-3]

    def dnfRecurse(self, nodes, direction, output):
        if self.label == None:
            newNodes = nodes
            newDirection = direction
            newOutput = output  
            newNodes.append(self)
            newDirection.append('0') 
            if self.is_nominal:
                for key in self.children: 
                    newDirection[-1] = str(key)
                    newOutput += self.children[key].dnfRecurse(newNodes, newDirection, output) 
            else:
                for i in [0,1]:
                    newDirection[-1] = str(i)
                    newOutput += self.children[i].dnfRecurse(newNodes, newDirection, output)
            return newOutput
        elif self.label == 1:
            newOutput = '('
            for i in range(0, len(nodes)):
                n = nodes[i]
                if n.is_nominal:
                    newOutput += n.name + '=' + direction[i] + ' ^ '
                elif int(direction[i]):
                    newOutput += n.name + '>=' + str(n.splitting_value) + ' ^ '
                else:
                    newOutput += n.name + '<' + str(n.splitting_value) + ' ^ '
            newOutput = newOutput[:-3] + ') v '
            return newOutput
        else:
            return ''

    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        nodes = []
        direction = []
        output = ''
        print self.dnfRecurse(nodes, direction, output)[:-3]


n3 = Node()
n3.label = 1
n3.name = 'oppWinPercentage'

n4 = Node()
n4.label = 0
n4.name = 'winPercentage'

n5 = Node()
n5.label = None
n5.decision_attribute = 1
n5.is_nominal = True
n5.name = "startingPitcher"
n5.children = {"Derek Jeter": n3, "Babe Ruth": n4}

n0 = Node()
n0.label = 1
n0.decision_attribute = 1
n0.name = 'homeOrAway'

n1 = Node()
n1.label = 0
n1.name = 'Temperature'

n = Node()
n.label = None
n.decision_attribute = 1
n.is_nominal = True
n.name = "weather"
n.children = {"sunny": n0, "rainy": n5}
n.print_dnf_tree()

    # def print_tree(self, indent = 0):
    #     '''
    #     returns a string of the entire tree in human readable form
    #     IMPLEMENTING THIS FUNCTION IS OPTIONAL
    #     '''
    #     # Your code here
    #     pass

    # def dnf_recurse(self, nodes, output):
    #     if (self.label == None):
    #         newNodes = nodes
    #         newNodes.append(self)
    #         newOutput = output
    #         for c in self.children:
    #             newOutput += self.children[c].dnf_recurse(newNodes, output)
    #         return newOutput
    #     elif (self.label == 1):
    #         newOutput = '('
    #         for n in nodes:
    #             if (n.decision_attribute != None):
    #                 if(n.is_nominal):
    #                     newOutput += n.name + '=' + str(n.decision_attribute) + ' ^ ' #questionable
    #                 else:
    #                     if(n.children[n.decision_attribute] == n.children[0].node):
    #                         newOutput += n.name + '<' + str(n.splitting_value) + ' ^ '
    #                     else:
    #                         newOutput += n.name + '>=' + str(n.splitting_value) + ' ^ '

    #         newOutput = newOutput[:-3] + ') v '
    #         return newOutput
    #     else:
    #         return '';