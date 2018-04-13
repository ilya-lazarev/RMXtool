#! python

"""
Count Restrictions ID on each edge.
Prints out edgeID, total # of restrictions, and list restrictions ID for that edge.
Run: $0 {<file>}+
"""

import sys
import pprint

class Restriction(object):
    def __init__(self, id):
        self.id = id
        self.starts = set()
        self.ends = set()

    def add_start_seg(self, seg):
        self.starts.add(seg)

    def add_end_seg(self, seg):
        self.ends.add(seg)


class Vut(object):
    def __init__(self, rec):
        self.code = rec[0]
        self.str1 = rec[1]
        self.str2 = rec[2]
        self.replace_ID()

    def replace_ID(self):
        if self.is_cat_dim('1', 'B'):
            if self.str1.startswith('DatasetID/'):
                self.str1 = self.str1[10:]
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


class Segment(object):
    """
    Represents on line of S(egment) record
    """
    def __init__(self, line, recs):
        self.vut = []
        self.line = line
        self.r_begins = set() #begins
        self.r_ends = set() #ends
        self.r_conts = set() # continuations
        (self.lon1, self.lat1, self.lon2, self.lat2) = recs[:4]
        recs = recs[4:]
        while len(recs) > 0:
            self.vut.append(Vut(recs))
            recs = recs[3:]
        self.collect_rids()

    def vut_num(self):
        return len(self.vut)

    def __str__(self):
        return [v.__str__() for v in self.vut].__str__()

    def get_edge_id(self):
        for v in self.vut:
            if v.str1 == 'EdgeID':
                return v.str2

    def collect_rids(self):
        for v in self.vut:
            if v.is_cat_dim('7', 'B') and v.str1[1] in 'PRpr':
                if v.str1[2] == 'B': # begin
                    self.r_begins.add(v.str2)
                elif v.str1[2] == 'E': #end
                    self.r_ends.add(v.str2)
                elif v.str1[2] == 'C': #continuation
                    self.r_conts.add(v.str2)

    def get_r_begins(self):
        return self.r_begins

    def get_r_ends(self):
        return self.r_ends

    def get_r_const(self):
        return self.r_conts

    def rids(self):   # generator
        for v in self.vut:
            if v.is_cat_dim('7', 'B') and v.str1[1] in 'PRpr':
                yield v
            # elif v.is_cat_dim('5', 'B'):
            #     yield v
    def __repr__(self):
        return "Segment: EdgeID="+self.get_edge_id()+" B:"+repr(self.r_begins)+" E:"+repr(self.r_ends)


def process_a(line, rec):
    if rec[0] == "Countries":
        print("Counties: " + rec[1])
    return None


def process_s(line, recs):
    if len(recs) < 5:
        print("S record < 5 fields")
        return None
    if (len(recs) - 4) % 3 != 0:
        print("Record not multiple of 3: ")
        return None
    return Segment(line, recs)


recordTypesMap = {'A': process_a, 'S': process_s}


def process_rmx(f):
    line = 0
    edges = {}
    rmap = {}
    print("Processing "+f)
    for l in open(f, "r"):
        line += 1
        type = l[0]
        recs = l.strip()[2:].split('|')[:-2]
        if type in recordTypesMap:
            r = recordTypesMap[type](line, recs)
            if r is None:
                continue
            e = r.get_edge_id()
            if e is None:
                continue
            if e not in edges:
                edges[e] = [set(),set()] # (begins, ends)

            rb = r.get_r_begins()
            re = r.get_r_ends()
            if len(rb) > 0:
                edges[e][0].update(rb)
            if len(re) > 0:
                edges[e][1].update(re)

            # add to dict by rid begins
            for ri in rb:
                if ri not in rmap:
                    rmap[ri] = [set(), set()]  # rid begins, rid ends
                rmap[ri][0].add(e)
            # add to dict by rid
            for ri in re:
                if ri not in rmap:
                    rmap[ri] = [set(), set()]  # rid begins, rid ends
                rmap[ri][1].add(e)

    print( "------------- BY EDGES ---------------")
    for (e, v) in edges.items():
        if len(v[0])>0 or len(v[1])>0:
            print("Edge "+e)
            print('   B: '+','.join(i for i in v[0])+', E: '+','.join(j for j in v[1]))

    print( "------------- BY RIDS ---------------")
    for (ri,v) in rmap.items():
        print("RID "+ri)
        print('   B: ' + ','.join(i for i in v[0]) + ', E: ' + ','.join(j for j in v[1]))

    print("Total length = {}, size = {}".format(len(edges), sys.getsizeof(edges)))
    print( "File {} done, {} lines".format(f, line))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        for f in sys.argv[1:]:
            process_rmx(f)
    else:
        print("Usage: " + sys.argv[0] + " {<file>}")

    print("=======DONE==========")
