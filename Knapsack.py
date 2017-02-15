from itertools import combinations

#items = (("map", 9, 150), ("compass", 13, 35), ("water", 153, 200), ("sandwich", 50, 160))
items = (
        ("map", 9, 150), ("compass", 13, 35), ("water", 153, 200), ("sandwich", 50, 160),
        ("glucose", 15, 60), ("tin", 68, 45), ("banana", 27, 60), ("apple", 39, 40),
        ("cheese", 23, 30), ("beer", 52, 10), ("suntan cream", 11, 70), ("camera", 32, 30),
        ("t-shirt", 24, 15), ("trousers", 48, 10), ("umbrella", 73, 40),
        ("waterproof trousers", 42, 70), ("waterproof overclothes", 43, 75),
        ("note-case", 22, 80), ("sunglasses", 7, 20), ("towel", 18, 12),
        ("socks", 4, 50), ("book", 30, 10),
        )

capacity = 150

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
    return (totval, -totwt) if totwt <= capacity else (0, 0)

def valuePerWeight(index):
    return items[index][2]/items[index][1]

def greedyEval(depth, value, weightRemaining, itemTaken):    
    if (itemTaken):
        value += items[depth][2]
        weightRemaining -= items[depth][1]
    
    for each in range(depth+1,len(items)):
        if (items[each][1] < weightRemaining):

            value += items[each][2]
            weightRemaining -= items[each][1]
    return value


def branchBound():
    decisionTree = [[0],[-1, greedyEval(0, 0, capacity, True), 0]]
    decisionTree.append([0, greedyEval(0, 0, capacity, True), items[0][2]])
    decisionTree.append([0, greedyEval(0, 0, capacity, False), 0])

    currentDepth = 0
    currentIndex = 1
    currentValue = 0
    capacityAvailable = capacity
    solution = False
    while (solution != True):
        #print currentDepth
        leftChild = 2 * currentIndex
        rightChild = (2 * currentIndex) + 1

        if (len(decisionTree)-3 < leftChild):
            while (len(decisionTree) < rightChild):
                decisionTree.append(0)
            decisionTree.insert(leftChild, [0, greedyEval(currentDepth, currentValue, capacityAvailable, True), items[currentDepth][2]])
            decisionTree.insert(rightChild, [0, greedyEval(currentDepth, currentValue, capacityAvailable, False), 0])

        #print "LeftChild = " + str(decisionTree[leftChild][1]) + " RightChild = " + str(decisionTree[rightChild][1])
        if ((decisionTree[leftChild][1] > decisionTree[rightChild][1]) & (capacityAvailable > items[currentDepth][1])):
            #print "Left"
            currentIndex = leftChild
            decisionTree[currentIndex][0]
            currentValue += decisionTree[currentIndex][2]
            capacityAvailable -= items[currentDepth][1]
        else:
            #print "Right"
            currentIndex = rightChild
            decisionTree[currentIndex][0]
            
        currentDepth += 1
        if (currentDepth > len(items)-1):
            print "Reached bottom of tree."
            solution = True
        
    print "Total Value is: " + str(currentValue)
        
def bruteForce():
    bagged = max( anycomb(items), key=totalvalue) # max val or min wt if values equal
    print("Bagged the following items\n  " +
          '\n  '.join(sorted(item for item,_,_ in bagged)))
    val, wt = totalvalue(bagged)
    print("for a total value of %i and a total weight of %i" % (val, -wt))
        
                        
    
    
branchBound()
bruteForce()

