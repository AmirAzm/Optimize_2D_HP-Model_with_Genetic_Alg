import numpy as np
import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y, label, action, dir):
        self.x = x
        self.y = y
        self.label = label
        self.action = action
        self.dir = dir

    def printN(self):
        print('('+str(self.x)+','+str(self.y)+') , '+self.label+' , '+self.action+' , '+self.dir)
        return
def en_f( nodes,alpha):
    c = 0
    for i,node in enumerate(nodes):
        if node.label == 'H':
            node_p = nodes[i+3:]
            for j in node_p:
                if j.label == 'H':
                    if (abs(node.x - j.x) == 0 and abs(node.y - j.y) == 1) or (abs(node.x - j.x) == 1 and abs(node.y - j.y) == 0):
                        c = c+1
    return c *alpha
def HH_C(S,A):
    A = A + "*"
    nodes = []
    valid = True
    nodes.append(Node(0, 0, S[0], A[0], '+x'))
    S = S[1:]
    A = A[1:]
    last = [nodes[0].x, nodes[0].y, nodes[0].action, nodes[0].dir]
    for s, a in zip(S, A):
        x = last[0]
        y = last[1]
        l_A = last[2]
        l_dir = last[3]
        if l_A == 'L' and l_dir == '+x':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'L' and l_dir == '-x':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'L' and l_dir == '+y':
            x = x - 1
            l_dir = '-x'
        elif l_A == 'L' and l_dir == '-y':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'F' and l_dir == '+x':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'F' and l_dir == '-x':
            x = x - 1
            l_dir = '-x'
        elif l_A == 'F' and l_dir == '+y':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'F' and l_dir == '-y':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'R' and l_dir == '+x':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'R' and l_dir == '-x':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'R' and l_dir == '+y':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'R' and l_dir == '-y':
            x = x - 1
            l_dir = '-x'
        if a == '*':
            l_dir = '*'
        for node in nodes:
            if (node.x, node.y) == (x, y):
                valid = False
        nodes.append(Node(x, y, s, a, l_dir))
        last = [x, y, a, l_dir]
    if valid:
        en = en_f(nodes, 1)
    else:
        # print('There are nodes that are overlap')
        en = 0
    return en
def generate_pop(n,m):
    pop = []
    while len(pop) != n:
        d = ''
        for i in range(m-1):
            d += genes[np.random.randint(0, 3)]
        t = {'seq': d, 'en': 0, 'p': 0, 'cum': 0}
        if HH_C(inp,t['seq']) != 0:
            pop.append(t)
    for ind in pop:
        ind['en'] = HH_C(inp, ind['seq'])
    return pop
def next_generte(pre):
    next_pop =[]
    n = len(pre)
    for i in range(n//2):
        ind1 =roulette(pre)
        ind2 =roulette(pre)
        ind1,ind2 = CrossOver(ind1,ind2)
        next_pop.append(ind1)
        next_pop.append(ind2)
    next_pop.sort(key=lambda x:x['en'],reverse=True)
    for ind in range(1,len(next_pop)):
        if random.random() <= mu_Th:
            Mutation(next_pop[ind])
    return next_pop
def roulette(pop):
    s = sum(ind['en'] for ind in pop)
    p_sum = 0
    for ind in pop:
        ind['p'] = ind['en'] / s
        p_sum += ind['p']
        ind['cum'] = p_sum
    R = random.random()
    for ind in pop:
        if ind['cum'] >= R:
            return ind
def CrossOver(p1,p2):
    flag = True
    s1,s2 ='',''
    e1,e2 =0,0
    chance = 0
    while flag:
        R = random.randint(0,len(p1['seq'])-1)
        s1 = p1['seq'][:R] + p2['seq'][R:]
        s2 = p2['seq'][:R] + p1['seq'][R:]
        e1  = HH_C(inp,s1)
        e2 = HH_C(inp,s2)
        if e1 != 0 and e2 != 0:
            flag =False
            c1 = {'seq': s1 , 'en': HH_C(inp,s1), 'p': 0, 'cum': 0}
            c2 = {'seq': s2 , 'en': HH_C(inp,s2), 'p': 0, 'cum': 0}
        chance += 1
        if chance == 20:
            flag =False
            c1 = p1
            c2 = p2
    return c1,c2
def Mutation(ind):
    R = random.randint(1,len(ind['seq'])-1)
    seq = list(ind['seq'])
    g = [x for i,x in enumerate(genes) if x!=seq[R]]
    seq[R] = g[np.random.randint(0,2)]
    ind['seq'] = ''.join(seq)
    return 0
def Tour(ind1,ind2):
    ind1['en'] = HH_C(inp, ind1['seq'])
    ind2['en'] = HH_C(inp, ind2['seq'])
    lst = [ind1,ind2]
    ind = max(lst,key=lambda x:x['en'])
    return ind
def plot_seq(S,A):
    Ares = A
    Sres = S
    A = A + "*"
    nodes = []
    nodes.append(Node(0, 0, S[0], A[0], '+x'))
    S = S[1:]
    A = A[1:]
    last = [nodes[0].x, nodes[0].y, nodes[0].action, nodes[0].dir]
    for s, a in zip(S, A):
        x = last[0]
        y = last[1]
        l_A = last[2]
        l_dir = last[3]
        if l_A == 'L' and l_dir == '+x':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'L' and l_dir == '-x':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'L' and l_dir == '+y':
            x = x - 1
            l_dir = '-x'
        elif l_A == 'L' and l_dir == '-y':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'F' and l_dir == '+x':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'F' and l_dir == '-x':
            x = x - 1
            l_dir = '-x'
        elif l_A == 'F' and l_dir == '+y':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'F' and l_dir == '-y':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'R' and l_dir == '+x':
            y = y - 1
            l_dir = '-y'
        elif l_A == 'R' and l_dir == '-x':
            y = y + 1
            l_dir = '+y'
        elif l_A == 'R' and l_dir == '+y':
            x = x + 1
            l_dir = '+x'
        elif l_A == 'R' and l_dir == '-y':
            x = x - 1
            l_dir = '-x'
        if a == '*':
            l_dir = '*'
        nodes.append(Node(x, y, s, a, l_dir))
        last = [x, y, a, l_dir]
        en = en_f(nodes,-1)
        x_s = []
        y_s = []
        for node in nodes:
            x_s.append(node.x)
            y_s.append(node.y)
            if node.label == 'H':
                plt.scatter(node.x, node.y, color='red', s=200, zorder=2)
            else:
                plt.scatter(node.x, node.y, color='blue', s=200, zorder=2)
        plt.plot(x_s, y_s, color='black', zorder=1, lw=5)
    plt.gca().set_aspect('equal')
    plt.title("En= " + str(en))
    plt.savefig('seq.png',dpi=300)
    plt.show()


inp = input('Enter HP sequence (H,P) :')
genes = ['F','R','L']
pop_size = int(input('Population Size :'))
generations = int(input('Number of Genertion :'))
mu_Th = 1e-4
pop = generate_pop(pop_size ,len(inp))
AVG = []
Max =[]
print(f'Genertion INIT')
for ind in pop:
    print(ind)
Max.append(max(pop, key=lambda x: x['en'])['en'])
AVG.append(sum(ind['en'] for ind in pop) / pop_size)
print('Max :', Max[0])
print('Average:', AVG[0])
for i in range(1,generations):
    print(f'Genertion {i}')
    pop = next_generte(pop)
    for ind in pop:
        print(ind)
    mx = max(pop, key=lambda x: x['en'])['en']
    Max.append(mx)
    avg = sum(ind['en'] for ind in pop) / pop_size
    AVG.append(avg)
    print('Max :', mx)
    print('Average:', avg)
pop.sort(key=lambda x: x['en'],reverse=True)
print(pop)
plot_seq(inp,pop[0]['seq'])
x = np.linspace(0,generations,generations)
fix = plt.figure()
ax = plt.axes()
ax.plot(x,AVG)
fix.savefig('Average.png',dpi=300)
fix.show()
fi =plt.figure()
bx = plt.axes()
bx.plot(x,Max)
fi.savefig('Max.png',dpi=300)
fi.show()


