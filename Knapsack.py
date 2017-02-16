#Branch and Bound code taken from:
#http://codereview.stackexchange.com/questions/94428/python-knapsack-problem-using-branch-and-bound-algorithm?rq=1

#Brutefroce code taken from:
#http://rosettacode.org/wiki/Knapsack_problem/0-1#Python

from itertools import combinations

data_item = ['map', 'compass', 'water', 'sandwich', 'glucose', 'tin', 'banana',
             'apple', 'cheese', 'beer', 'suntan', 'camera', 'T', 'trousers',
             'umbrella', 'w t', 'w o', 'note-case', 'sunglasses', 'towel',
             'socks', 'book']
data_weight = [9, 13, 153, 50, 15, 68, 27, 39, 23, 52, 11, 32, 24, 48, 73, 42,
               43, 22, 7, 18, 4, 30]
data_value = [150, 35, 200, 160, 60, 45, 60, 40, 30, 10, 70, 30, 15, 10, 40,
              70, 75, 80, 20, 12, 50, 10]
data_sorted = sorted(zip(data_item, data_weight, data_value),
                     key=lambda (i, w, v): v//w, reverse=True)

max_weight = 400


class State(object):
    def __init__(self, level, benefit, weight, token):
        # token = list marking if a task is token. ex. [1, 0, 0] means
        # item0 token, item1 non-token, item2 non-token
        # available = list marking all tasks available, i.e. not explored yet
        self.level = level
        self.benefit = benefit
        self.weight = weight
        self.token = token
        self.available = self.token[:self.level]+[1]*(len(data_sorted)-level)
        self.ub = self.upperbound()

    def upperbound(self):  # define upperbound using fractional knaksack
        upperbound = 0  # initial upperbound
        # accumulated weight used to stop the upperbound summation
        weight_accumulate = 0
        for avail, (_, wei, val) in zip(self.available, data_sorted):
            if wei * avail <= max_weight - weight_accumulate:
                weight_accumulate += wei * avail
                upperbound += val * avail
            else:
                upperbound += val * (max_weight - weight_accumulate) / wei * avail
                break
        return upperbound

    def develop(self):
        level = self.level + 1
        _, weight, value = data_sorted[self.level]
        left_weight = self.weight + weight
        if left_weight <= max_weight:  # if not overweighted, give left child
            left_benefit = self.benefit + value
            left_token = self.token[:self.level]+[1]+self.token[level:]
            left_child = State(level, left_benefit, left_weight, left_token)
        else:
            left_child = None
        # anyway, give right child
        right_child = State(level, self.benefit, self.weight, self.token)
        return ([] if left_child is None else [left_child]) + [right_child]

def branchBound():
    Root = State(0, 0, 0, [0] * len(data_sorted))  # start with nothing
    waiting_States = []  # list of States waiting to be explored
    current_state = Root
    while current_state.level < len(data_sorted):
        waiting_States.extend(current_state.develop())
        # sort the waiting list based on their upperbound
        waiting_States.sort(key=lambda x: x.ub)
        # explore the one with largest upperbound
        current_state = waiting_States.pop()
    best_item = [item for tok, (item, _, _)
                 in zip(current_state.token, data_sorted) if tok == 1]
    
    print "Total weight: ", current_state.weight
    print "Total Value: ", current_state.benefit
    print "Items:", best_item


def anycomb(items):
    ' return combinations of any length from the items '
    return ( comb
             for r in range(1, len(items)+1)
             for comb in combinations(items, r)
             )

def totalvalue(comb):
    ' Totalise a particular combination of items'
    totwt = totval = 0
    for item, wt, val in comb:
        totwt  += wt
        totval += val
    return (totval, -totwt) if totwt <= max_weight else (0, 0)

def bruteForce():
    bagged = max( anycomb(data_sorted), key=totalvalue) # max val or min wt if values equal
    print("Bagged the following items\n  " +
          ', '.join(sorted(item for item,_,_ in bagged)))
    val, wt = totalvalue(bagged)
    print("for a total value of %i and a total weight of %i" % (val, -wt))

bruteForce()
branchBound()
