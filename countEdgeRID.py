"""
Count Restrictions ID on each edge.
Prints out edgeID, total # of restrictions, and list restrictions ID for that edge.
Run: $0 {<file>}+
"""

import sys


class Vut:
    code = None
    str1 = None
    str2 = None

    def __init__(self, rec):
        i = 0
        self.code = rec[0]
        self.str1 = rec[1]
        self.str2 = rec[2]

    def __str__(self):
        return self.code + '|' + self.str1 + '|' + self.str2


class Record:
    line = 0
    vut = []

    def __init__(self, line, recs):
        self.line = line
        i = 0
        while len(recs) > 0:
            self.vut.append(Vut(recs))
            recs = recs[3:]

    def recordsNum(self):
        return len(self.vut)

    def __str__(self):
        return [v.__str__() for v in self.vut].__str__()


def processA(line, rec):
    if rec[0] == "Countries":
        print("Counties: " + rec[1])
    return


def processS(line, recs):
    if len(recs) < 5:
        print("S record < 5 fields")
        return
    (lon1, lat1, lon2, lat2) = recs[:4]
    recs = recs[4:]
    if len(recs) % 3 != 0:
        print("Record not multiple of 3: ")
    r = Record(line, recs)
    print("Record({}): {}".format(line, r))
    return


recordTypesMap = {'A': processA, 'S': processS}


def processRMX(f):
    line = 0
    for l in open(f, "r"):
        line += 1
        type = l[0]
        recs = l.strip()[2:].split('|')[:-2]
        if type in recordTypesMap:
            recordTypesMap[type].__call__(line, recs)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        for f in sys.argv[1:]:
            processRMX(f)
    else:
        print("Usage: " + sys.argv[0] + " {<file>}")

    print("=======DONE==========")
