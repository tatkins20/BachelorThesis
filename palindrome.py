def subpalindrome(s):

    if len(s) == 0 or len(s) == 1:
        return True
    elif s[0] == s[-1]:
        return subpalindrome(s[1:-1])
    else:
        return False




def palindrome(s):
    assert  1 <= len(s) <= 5000, "length not within range"
    for char in s:
        assert ord('a') <= ord(char) <= ord('z'), "char not in ascii range"
    substrings = []
    for grouplen in range(1, len(s)+1):
        for i in range(len(s)):
            slicedstring = s[i:i+grouplen]
            if slicedstring not in substrings:
                substrings.append(slicedstring)
    print(substrings)
    result = 0
    for item in substrings:
        if subpalindrome(item):
            result += 1
    return result


import math


def passing(filledTables):
    passedList = filledTables[:]

    indexOfmin = filledTables.index(min(filledTables))
    maxEntry = max(filledTables)

    for i in range(1, maxEntry):
        left = filledTables[indexOfmin - i]
        right = filledTables[indexOfmin + i]
        if isinstance(left, int):
            passedList[indexOfmin - i] = left + 1

        elif isinstance(right, int):
            passedList[indexOfmin - i] = right + 1

    if filledTables[0] == "M":
        if filledTables[1] != "M":
            passedList[0] = filledTables[1] + 1

    if filledTables[-1] == "M":
        if filledTables[-2] != "M":
            passedList[-1] = filledTables[-2] + 1

    for index in range(1, len(filledTables)-1):
        left = filledTables[index - 1]
        right = filledTables[index + 1]
        if isinstance(left, int) and isinstance(right, int):
            left += 1
            right += 1
            passedList[index] = min(left, right)
        elif isinstance(left, int):
            passedList[index] = left + 1
        elif isinstance(right, int):
            passedList[index] = right + 1
    print(passedList)
    return passedList


def maxHeight(tablePositions, tableHeights):
    filledTables = []
    hashtagHeights = []
    hashtagIndices = []
    for num in range(1, max(tablePositions)+1):
        if num in tablePositions:
            filledTables.append(num)
        else:
            filledTables.append("M")
    print(filledTables)
    counter = 0
    for index in range(len(filledTables)):
        if filledTables[index] != "M":
            filledTables[index] = tableHeights[counter]
            counter += 1
        else:
            hashtagIndices.append(index)
    print(filledTables)
    while "M" in filledTables:
        filledTables = passing(filledTables)

    for i in hashtagIndices:
        hashtagHeights.append(filledTables[i])

    return max(hashtagHeights)


def fountainranges(a):
    rangeList = []
    n = len(a)
    for i in range(n):
        j = i + 1
        ranges = (max(j - a[i], 1), min(j + a[i], n))
        rangeList.append(ranges)
    return rangeList

def fountaincoverage(tuples):
    solutions = []
    counter = 0
    for i in range(len(tuples)):
        if tuples[i][0] == 1:
            if tuples[i][1] == n:
                counter += 1
                solutions.append(counter)
            else:
                for j in range(i+1, len(tuples)):
                    if tuples[j][0] == tuples[i][1]:
                        counter += 1



if __name__ == '__main__':
    #print([4, "M", 3, "M", "M", "M", 3])
    #print(passing([4, "M", 3, "M", "M", "M", 3]))
    #print([1, "M", "M", "M", "M", "M", "M", 5])
    #print(passing([1, "M", "M", "M", "M", "M", "M", 5]))
    #print([5, "M", "M", 3, "M", "M", "M", 5, "M"])
    #print(passing([5, "M", "M", 3, "M", "M", "M", 5, "M"]))
    #print(maxHeight([1,10], [1,5]))
    print(fountaincoverage(["a", "b", "c", "d"]))
