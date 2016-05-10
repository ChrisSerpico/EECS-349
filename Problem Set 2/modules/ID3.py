import math
from node import Node
from collections import Counter
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
    maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    root = Node()
    root.label = None 
    if data_set == []:
        root.label = 0
        return root
    elif check_homogenous(data_set) != None:
        root.label = check_homogenous(data_set)
        return root
    elif (depth <= 0) or (len(data_set[0]) < 2):
        root.label = mode(data_set)
        return root
    else:
        attribute = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
        if not attribute[0]:
            root.label = mode(data_set)
            return root 
        root.name = attribute_metadata[attribute[0]]['name']
        root.is_nominal = attribute_metadata[attribute[0]]['is_nominal'] 
        root.decision_attribute = attribute[0] 
        if root.is_nominal:
            root.children = {} 
            vals = split_on_nominal(data_set, root.decision_attribute)
            
            for key in vals:
                depth -= 1 
                root.children[key] = ID3(vals[key], attribute_metadata, numerical_splits_count, depth)
        else:
            root.splitting_value = attribute[1]
            vals = split_on_numerical(data_set, root.decision_attribute, root.splitting_value)
            root.children = []
            numerical_splits_count[root.decision_attribute] -= 1 
            depth -= 1
            root.children.append(ID3(vals[0], attribute_metadata, numerical_splits_count, depth))
            root.children.append(ID3(vals[1], attribute_metadata, numerical_splits_count, depth))
    return root


def check_homogenous(data_set):
    # '''
    # ========================================================================================================
    # Input:  A data_set
    # ========================================================================================================
    # Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    # ========================================================================================================
    # Output: Return either the homogenous attribute or None
    # ========================================================================================================
     # '''
    check = 0
    for i in data_set:
        if i[0] is not None:
            check += i[0]
        else:
            return None
    if len(data_set) == check:
        return 1
    elif check == 0:
        return 0
    else:
        return None

# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    # '''
    # ========================================================================================================
    # Input:  A data_set, attribute_metadata, splits counts for numeric
    # ========================================================================================================
    # Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
    #         If nominal, then split value is False.
    #         If gain ratio of all the attributes is 0, then return False, False
    #         Only consider numeric splits for which numerical_splits_count is greater than zero
    # ========================================================================================================
    # Output: best attribute, split value if numeric
    # ========================================================================================================
    # '''
    steps = 1
    maxGainRatio = 0
    bestAttribute = False
    bestSplitValue = False
    for attribute in range(1, len(attribute_metadata)):
        n = attribute_metadata[attribute]
        if n['is_nominal']:
            grn = gain_ratio_nominal(data_set, attribute)
            if grn > maxGainRatio:
                maxGainRatio = grn
                bestAttribute = attribute
                bestSplitValue = False
        elif numerical_splits_count[attribute] != 0:
            grn, split_value = gain_ratio_numeric(data_set, attribute, steps)
            if grn > maxGainRatio:
                maxGainRatio = grn
                bestAttribute = attribute
                bestSplitValue = split_value
    if maxGainRatio == 0:
        bestAttribute = False
    return bestAttribute, bestSplitValue

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    # '''
    # ========================================================================================================
    # Input:  A data_set
    # ========================================================================================================
    # Job:    Takes a data_set and finds mode of index 0.
    # ========================================================================================================
    # Output: mode of index 0.
    # ========================================================================================================
    # '''
    dataList = []
    for i in data_set:
        dataList.append(i[0])
    data = Counter(dataList)
    mode = data.most_common(1)
    mode = mode[0]
    return mode[0]
    
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    # '''
    # ========================================================================================================
    # Input:  A data_set
    # ========================================================================================================
    # Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    # ========================================================================================================
    # Output: Returns entropy. See Textbook for formula
    # ========================================================================================================
    # '''
    count = 0
    for i in data_set:
            if i[0] == 1:
                count += 1
    length = len(data_set)
    percentage = float(count)/float(length)
    percentage2 = 1 - percentage
    if count == length or count == 0:
        return 0
    else:
        entropy = -(percentage2*math.log(percentage2,2)+percentage*math.log(percentage,2))
        return entropy

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def intrinsic_val(data):
    #takes in a list of the amounts of each atribute and calculates the intrisic value
    total = sum(data)
    in_val = 0
    for i in data:
        fract = float(i)/float(total)
        in_val += -(fract)*math.log(fract,2)
    return in_val

def gain_ratio_nominal(data_set, attribute):
    # '''
    # ========================================================================================================
    # Input:  Subset of data_set, index for a nominal attribute
    # ========================================================================================================
    # Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    # ========================================================================================================
    # Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    # ========================================================================================================
    # '''
    lengthList = []
    data_set_out = []
    tot = 0
    splitDict = split_on_nominal(data_set,attribute)
    outputList = []
    for i in splitDict:
        split_list = splitDict[i]
        lengthList.append(len(split_list))
        for i in split_list:
            outputList.append([i[0]])
        tot += (((float(len(outputList))/float(len(data_set)))) * entropy(outputList))
        outputList = []
    for i in data_set:
        data_set_out.append([i[0]])
    info_gain = entropy(data_set_out) - tot
    in_val = intrinsic_val(lengthList)
    return info_gain/in_val

# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    # '''
    # ========================================================================================================
    # Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    # ========================================================================================================
    # Job:    Calculate the gain_ratio_numeric and find the best single threshold value
    #         The threshold will be used to split examples into two sets
    #              those with attribute value GREATER THAN OR EQUAL TO threshold
    #              those with attribute value LESS THAN threshold
    #         Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
    #         And restrict your search for possible thresholds to examples with array index mod(step) == 0
    # ========================================================================================================
    # Output: This function returns the gain ratio and threshold value
    # ========================================================================================================
    # '''
    counter = 0
    bestGain = 0
    bestThreshold = 0
    posThreshold = []
    testThreshold = []
    numThreshold = math.floor(len(data_set)/steps)
    split_list = []
    ratio_list = []
    ratio_dict = {}
    for i in data_set:
        posThreshold.append(i[attribute])
    while counter <= numThreshold:
        if counter*steps is not len(data_set):
            testThreshold.append(posThreshold[(counter*steps)])
            counter += 1
        else:
            counter += 1
    for i in testThreshold:
        threshold = i
        for k in data_set:
            if k[attribute] < threshold:
                split_list.append([k[0],1])
            else:
                split_list.append([k[0],2])
        splitDict = split_on_nominal(split_list,1)
        if len(splitDict) > 1:
            ratio_dict[gain_ratio_nominal(split_list,1)] = threshold
            gain = gain_ratio_nominal(split_list,1)
            ratio_list.append(gain)
            split_list = []
        else:
            split_list = []
    if ratio_list != []:
        bestGain =  max(ratio_list)
        bestThreshold = ratio_dict[bestGain]
    return (bestGain,bestThreshold)

# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    # '''
    # ========================================================================================================
    # Input:  subset of data set, the index for a nominal attribute.
    # ========================================================================================================
    # Job:    Creates a dictionary of all values of the attribute.
    # ========================================================================================================
    # Output: Dictionary of all values pointing to a list of all the data with that attribute
    # ========================================================================================================
    # '''
    d = {}
    
    for i in data_set:
        val=i[attribute]
        d[val] = []
        
    for i in data_set:
        val = i[attribute]
        d[val].append(i)
    return d
    
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    # '''
    # ========================================================================================================
    # Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    # ========================================================================================================
    # Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
    # attribute has value less than the splitting value, the second list contains the other examples
    # ========================================================================================================
    # Output: Tuple of two lists as described above
    # ========================================================================================================
    # '''
    lessList = []
    elseList = []
    
    for i in data_set:
        val = i[attribute]
        if val < splitting_value:
            lessList.append(i)
        else:
            elseList.append(i)
    split = (lessList,elseList)
    return split

# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
