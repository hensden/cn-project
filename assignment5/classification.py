from copy import deepcopy as dc
import datetime

class Node:
    left = None
    right = None
    next_trie = None

    def __str__(self):
        return "(Left:%s  Right:%s Next:%s)" % (str(self.left), str(self.right), str(self.next_trie))
    def __repr__(self):
        return self.__str__()

root = Node()

class Rule:
    def __init__(self, number, cost):
        self.number = number
        self.cost = cost

    def __str__(self):
        return "Rule number:%d Cost:%d" % (self.number, self.cost)
    def __repr__(self):
        return self.__str__()
    def __lt__(self, other):
        return self.cost < other.cost

def dfs(A,B):
    if A.left == None and B.left:
        A.left = B.left
    if A.right == None and B.right:
        A.right = B.right
    if A.left and B.left:
        dfs(A.left, B.left)
    if A.right and B.right:
        dfs(A.right, B.right)

def mergeTries(A, B):
    if A == None and B != None:
        return B
    elif A != None and B == None:
        return A
    elif A == None and B == None:
        return None
    else:
        dfs(A,B)
        return A

def addRule(rule, t1, t2):
    node = root
    new_next_trie = dc(root.next_trie)
    for i in t1:
        if i == '0':
            if node.left is None:
                node.left = Node()
            node = node.left
        elif i == '1':
            if node.right is None:
                node.right = Node()
            node = node.right
        new_next_trie = mergeTries(dc(new_next_trie), dc(node.next_trie))
    
    node.next_trie = dc(new_next_trie)
    if node.next_trie is None:
        node.next_trie = Node()
    node = node.next_trie
    for i in t2:
        if i == '0':
            if node.left is None:
                node.left = Node()
            node = node.left
        elif i == '1':
            if node.right is None:
                node.right = Node()
            node = node.right
    if node.next_trie is None:
        node.next_trie = rule

def classify(t1, t2):
    possible_rules = []
    node = root
    for i in t1:
        if i == '0':
            if node.left is None:
                break
            node = node.left
        elif i == '1':
            if node.right is None:
                break
            node = node.right
    node = node.next_trie
    if node is None:
        return []
    for i in t2:
        if node.next_trie is not None:
            possible_rules.append(node.next_trie)
        if i == '0':
            if node.left is None:
                break
            node = node.left
        elif i == '1':
            if node.right is None:
                break
            node = node.right
    if node.next_trie is not None:
        possible_rules.append(node.next_trie)
    return list(set(possible_rules))



for index, line in enumerate(open("rules.txt")):
    rule, t1, l1, t2, l2 = line.split(" ")
    rule = int(rule)
    l1 = int(l1)
    l2 = int(l2)
    bin_t1 =  "".join([ "%08d" % int(str(bin(int(i)))[2:]) for i in t1.split(".") ])
    bin_t2 =  "".join([ "%08d" % int(str(bin(int(i)))[2:]) for i in t2.split(".") ])
    bin_t1 = bin_t1[:l1]
    bin_t2 = bin_t2[:l2]
    addRule(Rule(rule, index), bin_t1, bin_t2)

with open("output.txt", 'w') as O:
    for index, line in enumerate(open("input")):
        t1, t2 = line.strip().split(" ")
        bin_t1 =  "".join([ "%08d" % int(str(bin(int(i)))[2:]) for i in t1.split(".") ])
        bin_t2 =  "".join([ "%08d" % int(str(bin(int(i)))[2:]) for i in t2.split(".") ])
        m1 = float(datetime.datetime.now().microsecond)
        possible_rules = classify(bin_t1, bin_t2)
        m2 = float(datetime.datetime.now().microsecond)
        if possible_rules == []:
            O.write('%s %s %d %d %.1f\n' % (t1, t2, len(possible_rules), -1,m2-m1))
        else:
            O.write('%s %s %d %d %.1f\n' % (t1, t2, len(possible_rules), min(possible_rules).number,m2-m1))
