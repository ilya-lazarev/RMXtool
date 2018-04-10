"""
Count Restrictions ID on each edge.
Prints out edgeID, total # of restrictions, and list restrictions ID for that edge.
Run: $0 {<file>}+
"""

import sys


class Rectrictions:
    def __init__(self, id):
        self.id = id
        self.starts = set()
        self.ends = set()

    def add_start_seg(self, s: Record):
        self.starts.add(s)

    def add_end_seg(self, s: Record):
        self.ends.add(s)

class Vut:
    def __init__(self, rec):
        i = 0
        self.code = rec[0]
        self.str1 = rec[1]
        self.str2 = rec[2]
        self.replace_ID()

    def replace_ID(self):
        if self.is_cat_dim('1', 'B'):
            if self.str1.startswith('DatasetID/'):
                self.str1 = self.str1[10:]
            if self.str1 == 'EdgeID':
                self.str2 = self.str2.replace('/', '')
                print("Replaced EdgeID"+self.str2)

    def __str__(self):
        return self.code + '|' + self.str1 + '|' + self.str2

    def priority(self):
        return None if self.code is None else self.code[0]

    def category(self):
        return None if self.code is None else self.code[1]

    def dimension(self):
        return None if self.code is None else self.code[2]

    def direction(self):
        return None if self.code is None else self.code[3]

    def is_cat_dim(self, cat, dim):
        return False if self.code is None else (self.code[1] == cat and self.code[2] == dim)


class Record:
    """
    Represents on line of S(egment) record
    """
    def __init__(self, line, recs):
        self.vut = []
        self.line = line
        (self.lon1, self.lat1, self.lon2, self.lat2) = recs[:4]
        recs = recs[4:]
        while len(recs) > 0:
            self.vut.append(Vut(recs))
            recs = recs[3:]

    def vut_num(self):
        return len(self.vut)

    def __str__(self):
        return [v.__str__() for v in self.vut].__str__()

    def get_edge_id(self):
        for v in self.vut:
            if v.str1 == 'EdgeID':
                return v.str2

    def collect

def process_a(line, rec):
    if rec[0] == "Countries":
        print("Counties: " + rec[1])
    return None


def process_s(line, recs):
    if len(recs) < 5:
        print("S record < 5 fields")
        return
    if (len(recs) - 4) % 3 != 0:
        print("Record not multiple of 3: ")
    return Record(line, recs)


recordTypesMap = {'A': process_a, 'S': process_s}


def process_rmx(f):
    line = 0
    edges = {}
    for l in open(f, "r"):
        line += 1
        type = l[0]
        recs = l.strip()[2:].split('|')[:-2]
        if type in recordTypesMap:
            r = recordTypesMap[type].__call__(line, recs)
            if r is not None:
                pass
    print( "File {} done, {} lines".format(f, line))



if __name__ == "__main__":
    if len(sys.argv) >= 2:
        for f in sys.argv[1:]:
            process_rmx(f)
    else:
        print("Usage: " + sys.argv[0] + " {<file>}")

    print("=======DONE==========")
