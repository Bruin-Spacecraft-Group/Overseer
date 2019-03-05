#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 19:44:06 2019

@author: katsuyamamorito
"""
def Find_Latest_Coordinate(): 
    with open("terminaloutputgps.txt") as data:
        l = data.readlines()
    
    linenumber = len(l)
    
    line_format = False        #whether the index has proper format or not
    Index_check = linenumber-1
    
    while line_format == False:
        splittedline = l[Index_check].split(",")
        if splittedline[0] == "$$OVERSEER":
            latitude = splittedline[3]
            longitude = splittedline[4]
            line_format = True
        else:
            Index_check = Index_check - 1
    return latitude,longitude
            
#It should eliminate if the coordinate is (0,0)
coordinate = Find_Latest_Coordinate()

          
