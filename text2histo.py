#!/usr/bin/env python
"""
Takes lines of integers (or characters whose length is notable) and
displays a histogram of the occurence frequencies of the integer (or
of the length of the lines' characters).

Examples

$ text2histo.py 1 1 2 3 3 3 4 4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5  5 6 6 6 7 8 8 9 12
   12 ..  10.8 | [ 1] #
 10.8 ..   9.6 | [ 0] 
  9.6 ..   8.4 | [ 1] #
  8.4 ..   7.2 | [ 2] ##
  7.2 ..   6.0 | [ 1] #
  6.0 ..   4.8 | [21] #####################
  4.8 ..   3.6 | [ 2] ##
  3.6 ..   2.4 | [ 3] ###
  2.4 ..   1.2 | [ 1] #
  1.2 ..     1 | [ 2] ##

$ text2histo.py --bins=5 1 1 2 3 3 3 4 4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5  5 6 6 6 7 8 8 9 12
  12 ..  9.6 | [ 1] #
 9.6 ..  7.2 | [ 3] ###
 7.2 ..  4.8 | [22] ######################
 4.8 ..  2.4 | [ 5] #####
 2.4 ..    1 | [ 3] ###


$ head ~/src/stopwords.txt
a
about
above
across
after
again
against
all
almost
alone

$ head ~/src/stopwords.txt | text2histo.py
   7 ..  5.6 | [3] ###
 5.6 ..  4.2 | [5] #####
 4.2 ..  2.8 | [1] #
 2.8 ..  1.4 | [0] 
 1.4 ..    1 | [1] #


"""

import math
import optparse
import os
import sys



def get_counts(lines):
    """returns a dict of integer -> occurrence count"""

    counts = {}

    for line in lines:
        line = line.strip()

        try:
            count = int(line)
        except Exception, msg:
            count = len(line)

        if count not in counts:
            counts[count] = 0

        counts[count] = counts[count] + 1

    return counts


def get_bin_contents(counts, bins=None):
    """returns a list of bin_start, bin_end, size lists"""
    max_c = max(counts.keys())
    min_c = min(counts.keys())

    if bins is None:
        bins = min(20, len(counts.keys()))
    else:
        bins = int(bins) # in case it's a string

    bin_range = (max_c - min_c) + 1
    bin_increment = bin_range / math.ceil(float(bins))

    bin_start = max_c

    bin_contents = []
    for i in range(bins):

        last_bin = i == bins - 1

        if last_bin:
            bin_end = min_c
        else:
            bin_end = bin_start - bin_increment

        size = sum([counts[c] for c in counts
                    if ((c <= bin_start)
                        and
                        ((c > bin_end) or (last_bin and c == bin_end)))])

        bin_contents.append([bin_start, bin_end, size])
        bin_start = bin_end

    return bin_contents


def print_histogram_bins(bin_contents):
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

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("--bins", default=None)
    options, args = parser.parse_args()

    if (len(args) > 0) and ("-" not in args):
        lines = args
    else:
        lines = sys.stdin.readlines()

    counts = get_counts(lines)

    bin_contents = get_bin_contents(counts, bins=options.bins)

    print_histogram_bins(bin_contents)
