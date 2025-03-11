# Write a function, which when iven one string (s) and two characters
# (c1 and c2), computes all pairings of contiguous ranges of c1s
# and c2s that have the same length.  Your function should return
# a set of three-tuples.  Each element of the set should be
# (c1 start index, c2 start index, length)
#
# Note that s may contain other characters besides c1 and c2.
# Example:
#  s = abcabbaacabaabbbb
#      01234567890111111  <- indices for ease of looking
#                1123456
#  c1 = a
#  c2 = b
#  Observe that there are the following contiguous ranges of 'a's (c1)
#  Length 1: starting at 0, 3, 9
#  Length 2: starting at 6, 11
#  And the following contiguous ranges of 'b's (c2)
#  Length 1: starting at 1, 10
#  Length 2: starting at 4
#  Length 4: starting at 13
#  So the answer would be
#  { (0, 1, 1), (0, 10, 1), (3, 1, 1), (3, 10, 1), (9, 1, 1), (9, 10, 1),
#    (6, 4, 2), (11, 4, 2)}
#  Note that the length 4 range of 'b's does not appear as there are no
#  Length 4 runs of 'a's.
from datetime import datetime
import random
import time

# Prints a list of integers with specific formatting
def printInt(data):
    for i in data:
        print("%7d" % i, ",", sep="", end="")

# Prints a list of floats with specific formatting
def printFloat(data):
    for i in data:
        print("%2.5f" % i, ",", sep="", end="")

# Finds matching substrings with specified characters (c1, c2) in the input string
def matching_length_sub_strs(s, c1, c2):
    dic_c1, dic_c2 = {}, {}
    cnt1, cnt2 = 0, 0

    # Helper function to update the dictionary with matching lengths
    def update_dict(dic, key, value):
        if key in dic:
            dic[key].append(value)
        else:
            dic[key] = [value]

    # Iterate over the string to find matching lengths
    for i in range(len(s)):
        if s[i] == c1:
            cnt1 += 1
            if cnt2 != 0:
                update_dict(dic_c2, cnt2, i - cnt2)
                cnt2 = 0
        elif s[i] == c2:
            cnt2 += 1
            if cnt1 != 0:
                update_dict(dic_c1, cnt1, i - cnt1)
                cnt1 = 0
        else:
            if cnt1 != 0:
                update_dict(dic_c1, cnt1, i - cnt1)
                cnt1 = 0
            if cnt2 != 0:
                update_dict(dic_c2, cnt2, i - cnt2)
                cnt2 = 0
    if cnt1 != 0:
        update_dict(dic_c1, cnt1, len(s) - cnt1)
    if cnt2 != 0:
        update_dict(dic_c2, cnt2, len(s) - cnt2)

    ans = set()
    # Find the matching lengths from both dictionaries and return as a set of tuples
    for i in dic_c1:
        if i in dic_c2:
            for j in dic_c1[i]:
                for k in dic_c2[i]:
                    ans.add((j, k, i))

    return ans

# Generates a random string of length n, mostly consisting of 'a' and 'b'
def rndstr(n):
    def rndchr():
        x = random.randrange(7)
        if x == 0:
            return chr(random.randrange(26) + ord('A'))
        if x <= 3:
            return 'a'
        return 'b'

    ans = [rndchr() for i in range(n)]
    return "".join(ans)

# Generates a "best" case string where 'a' and 'b' are grouped together
def beststr(n):
    def rndchr():
        x = random.randrange(2)
        if x == 0:
            return 'a'
        return 'b'

    lena = random.randrange(1, n + 1)
    ans = []
    ans.extend([rndchr()] * lena)
    ans.extend([rndchr()] * (n - lena))
    return "".join(ans)

# Generates a "worst" case string with alternating 'a' and 'b'
def worststr(n):
    x = random.randrange(2)
    ans = ""
    if x == 0:
        ans += "ab" * int(n / 2)
        if n % 2 == 1:
            ans += "a"
    else:
        ans += "ba" * int(n / 2)
        if n % 2 == 1:
            ans += "b"
    return ans

if __name__ == '__main__':
    c1, c2 = 'a', 'b'

    # Define data sizes for testing
    data_size = []
    cnt = 1
    while (cnt * 512 <= 16384):
        data_size.append(cnt * 512)
        cnt *= 2
    printInt(data_size)

    data_best, data_worst, data_rnd = [], [], []

    # Measure and store execution times for best case
    for size in data_size:
        s_best = beststr(size)
        start = time.perf_counter()
        ans = matching_length_sub_strs(s_best, c1, c2)
        end = time.perf_counter()
        data_best.append(end - start)
    printFloat(data_best)
    print()

    # Measure and store execution times for worst case
    for size in data_size:
        s_worst = worststr(size)
        start = time.perf_counter()
        ans = matching_length_sub_strs(s_worst, c1, c2)
        end = time.perf_counter()
        data_worst.append(end - start)
    printFloat(data_worst)
    print()

    # Measure and store execution times for random case
    for size in data_size:
        s_rnd = rndstr(size)
        start = time.perf_counter()
        ans = matching_length_sub_strs(s_rnd, c1, c2)
        end = time.perf_counter()
        data_rnd.append(end - start)
    printFloat(data_rnd)
    print()

    # Test with a random string of length 15
    s_rnd = rndstr(15)
    ans = matching_length_sub_strs(s_rnd, c1, c2)
    print(s_rnd)
    print(ans)


    
