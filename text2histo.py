#!/usr/bin/env python
"""
Example

$ seq 1 15 | text2histo.py



$ text2histo.py 1 1 2 3 3 3 4 4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 6 6 6 7 8 8 9 12
   12 ..  10.8 | [ 1] #
 10.8 ..   9.6 | [ 0] 
  9.6 ..   8.4 | [ 1] #
  8.4 ..   7.2 | [ 2] ##
  7.2 ..   6.0 | [ 1] #
  6.0 ..   4.8 | [21] #####################
  4.8 ..   3.6 | [ 2] ##
  3.6 ..   2.4 | [ 3] ###
  2.4 ..   1.2 | [ 1] #
  1.2 ..     1 | [ 0] 


"""

import datetime, sys, os, math


if "--help" in sys.argv:
    print __doc__
    sys.exit(1)


counts = {}

if len(sys.argv[1:]) > 1:
    lines = sys.argv[1:]
else:
    lines = sys.stdin.readlines()

def get_counts(lines):
    for line in lines:
        count = None
        label = None

        line = line.strip()
        try:
            label = int(line)
            count = 1
        except Exception, msg:
            try:
                first, second = line.split()
                count, label = int(first), second
            except Exception, msg:
                #label = len(line)
                label = line
                count = 1

        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + count


def get_histogram_lines(counts):
    bins = min(20, len(counts.keys()))

    max_c = max(counts.values())
    min_c = min(counts.values())

    bin_range = (max_c - min_c) + 1
    bin_increment = bin_range / math.ceil(float(bins))

    bin_contents = []
    bin_start = max_c
    for i in range(bins):
        if i == bins - 1:
            bin_end = min_c
        else:
            bin_end = bin_start - bin_increment
        size = sum([counts[c] for c in counts
                    if (c <= bin_start) and (c > bin_end)])
        bin_contents.append([bin_start, bin_end, size])
        bin_start = bin_end

bin_start_and_ends = reduce(lambda a, b: a + b,
                            [[s, e] for s, e, size in bin_contents], [])
bin_label_padding = max(map(len, map(str, bin_start_and_ends))) + 1
size_padding = max([len(str(size)) for s, e, size in bin_contents])
format_str = "%%%ds .. %%%ds | [%%%ds] %%s\n" % (bin_label_padding,
                                                 bin_label_padding,
                                                 size_padding)

for bin_start, bin_end, size in bin_contents:
    sys.stdout.write(format_str % (bin_start,
                                   bin_end,
                                   size,
                                   "#" * size))
