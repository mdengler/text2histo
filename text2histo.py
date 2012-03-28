#!/usr/bin/env python
"""
Example

seq 1 15 | text2histo.py

"""

import datetime, sys, os, math


if "--help" in sys.argv:
    print __doc__
    sys.exit(1)


counts = {}

for line in sys.stdin.readlines():
    line = line.strip()
    try:
        count = int(line)
    except Exception, msg:
        count = len(line)

    if count not in counts:
        counts[count] = 0
    counts[count] = counts[count] + 1

max_c = max(counts.keys())
min_c = min(counts.keys())

bins = 20
bin_range = (max_c - min_c)
bin_increment = bin_range / math.ceil(float(bins))

bin_start = max_c
bin_increment = (max_c - min_c) / bins
for i in range(bins):
    bin_end = bin_start - bin_increment
    size = len([c for c in counts if (c <= bin_start) and (c > bin_end)])
    print "%10s .. %10s | [%5s] %s" % (bin_start,
                                       bin_end,
                                       size,
                                       "#" * size)
    bin_start = bin_end

bin_end = min_c
size = len([c for c in counts if (c <= bin_start) and (c > bin_end)])
print "%10s .. %10s | [%5s] %s" % (bin_start,
                                   bin_end,
                                   size,
                                   "#" * size)









"""
sub show_histogram
{
   # Prints a simple text histogram given a reference
   # to an array of integers.
   # Larry Leszczynski <larryl@furph.com>

   my ($array_ref, $binsize, $width) = @_;
   $binsize ||= 1;
   $width   ||= 50;

   use POSIX qw(ceil floor);

   # Divide input data into bins:
   my %bin_count = ();   # number of items in each bin
   foreach ( @$array_ref ) {
      my $bin = floor(($_+.5)/$binsize);
      $bin_count{$bin}++;
   }

   my $max_items = 0;   # maximum items in a single bin
   foreach ( values %bin_count ) {
      $max_items = $_ if $_ > $max_items;
   }

   # Try to keep histogram on one page width:
   my $scale = 1;
   if ( $max_items > $width ) {
      if ( $max_items <= ($width*5) ) {
         $scale = 5;
      }
      else {
         while ( ($max_items/$scale) > $width ) {
            $scale *= 10;
         }
      }
   }

   my @bins   = sort {$a <=> $b} keys %bin_count;
   my $bin    = $bins[0];    # lowest value bin
   my $maxbin = $bins[-1];   # highest value bin

   my $binfmt_width = ( length $maxbin > length $bin )
                      ? length $maxbin : length $bin;
   my $cntfmt_width = length $max_items;

   my $start = $bin * $binsize;
   my $end   = $start + $binsize - 1;
   do {
      my $count = $bin_count{$bin} || 0;
      my $extra = ( $count % $scale ) ? '.' : '';
      printf "%*d .. %*d  \[%*d\] %s$extra\n",
                    $binfmt_width, $start,
                    $binfmt_width, $end,
                    $cntfmt_width, $count,
                    '#' x ceil($count/$scale);
      $start += $binsize;
      $end   += $binsize;
   } while ( $bin++ < $maxbin );
   print "\n  Scale: #=$scale\n" if $scale > 1;
}
"""
