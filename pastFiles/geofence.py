#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 20:25:06 2018

@author: katsuyamamorito
"""
import csv

# Open geofence csv file
f = open('geofence.csv','r',encoding = 'utf-8-sig')  # CSV with BOM
lst = list(csv.reader(f))
# Close the file
f.close();

# Convert elements of array from string to float
for i in range(len(lst)):
    lst[i][0] = float(lst[i][0])
    lst[i][1] = float(lst[i][1])

# Initialize an array that stores start point and end point of lines
lines = [0]*len(lst)
for i in range(len(lst)-1):
    lines[i] = [lst[i],lst[i+1]]
lines[len(lst)-1] = [lst[len(lst) - 1],lst[0]]

# Check if coords are in or out of Safety zone
def inorout(latitude,longitude):
    count = 0   # The number of boundaries
    for i in range(len(lines)):

        lat0 = lines[i][0][0]
        lat1 = lines[i][1][0]
        lon0 = lines[i][0][1]
        lon1 = lines[i][1][1]

        if (lat0 - latitude)*(lat1 - latitude) < 0:
            # The point is positioned between two nodes of the line
            if lon1 == lon0:    # When the denominator of slope is 0
                if lon1 > longitude:
                    count = count + 1
                continue

            slope = (lat1 - lat0) / (lon1 - lon0)

            val = slope*(longitude - lon0) + lat0

            if slope > 0:
                if latitude > val:
                    count = count + 1
            if slope < 0:
                if latitude < val:
                    count = count + 1


    if (count % 2) == 1:    # S/c is in the Safety zone
        return True
    else:                   # S/c is in the Danger zone
        return False


k = inorout(33.43,-114.502)
