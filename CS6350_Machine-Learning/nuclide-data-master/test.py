#!/usr/bin/python
from __future__ import print_function, division
import nuclide_data
from masstable import Table

# Max protons = 117
max_protons = 117
ame = Table("AME2012")
for i in xrange(0, max_protons):
    temp = ame[i,:]
    print(temp)
#print(temp)
#print(nuclide_data.nuc(7,15))
