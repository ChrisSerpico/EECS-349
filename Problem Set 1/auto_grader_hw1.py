total = 0
from PS1 import *

options = {
	'get_value': True,
	'get_children': True,
	'bfs': True,
}

def grader(get_value = False, get_children = False, bfs = False):
	title = '==========='
	
	if get_value:
		name = 'get_value_test'
		total = 0
		node1 = Node()
		node2 = Node()
		node1.value = 5
		node2.value = 9996
		if(node1.get_value() == 5):
			total += 0
			print 'Passed first get_value_test'
		else:
			print 'Failed first get_value test'
		if(node2.get_value() == 9996):
			total += 1
			print 'Passed second get_value test'
		else:
			print 'Failed second get_value test'

	if get_children:
		name = 'get_children'
		node_list = []
		node_vals = [1,2,3,4,5]
		a = Node()
		a.value = 1
		b = Node()
		b.value = 2
		c = Node()
		c.value = 3
		d = Node()
		d.value = 4
		e = Node()
		e.value = 5
		a.children = {1: b, 2: c, 3: d}
		c.children = {1: e}
		if(a.get_children() == a.children):
			total += 0
			print 'Passed first get children test'
		else:
			print 'Failed first get children test'
		if(b.get_children() == b.children):
			total += 1
			print 'Passed second get children test'
		else:
			print 'Failed second get children test'
		if(c.get_children() == c.children):
			total += 1
			print 'Passed third get children test'
		else:
			print 'Failed third get children test'

	if bfs:
		name = 'bfs'
		node_list = []
		node_vals = [6,7,8,9,10]
		f = Node()
		f.value = 6
		g = Node()
		g.value = 7
		h = Node()
		h.value = 8
		i = Node()
		i.value = 9
		j = Node()
		j.value = 10

		a.children = {1: b, 2: c, 3: d}
		c.children = {1: e, 2: f}
		d.children = {1: g}
		e.children = {1: h, 2: i}
		f.children = {1: j}

		if breadth_first_search(a) == '1 2 3 4 5 6 7 8 9 10' or breadth_first_search(a) == '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]':
			total += 3
			print 'Passed first bfs test'
		else:
			print 'Failed first bfs test'
		
		x = Node()
		x.value = 26
		y = Node()
		y.value = 15
		z = Node()
		z.value = 25
		t = Node()
		t.value = 100

		x.children = {1: z}
		z.children = {1: t, 2: y}

		if breadth_first_search(x) == '26 25 100 15' or breadth_first_search(a) == '[26, 25, 100, 15]':
			total += 3
			print 'Passed second bfs test'
		else:
			print 'Failed second bfs test'
	print 'Total Score: ' + str(total) + '/9'
	print(total)
test = grader( **options )

