from __future__ import print_function
from array import *

#processing data: analysis
def process_data(source_file, target_file, time_interval):
    #word counter
    count_slut = int(0)
    count_rape = int(0)
    count_whore = int(0)
    
    #result arrays
    rape_arr = array('I')
    slut_arr = array('I')
    whore_arr = array('I')

    #open file and create list with all entries
    entry_list = list()
    file = open(source_file,"r")
    for line in file:
        #implode string by delimiter
        temp_string = line.split('|')
        
        #append each line as list entry
        entry_list.append([temp_string[1],temp_string[0],temp_string[2]])

    file.close()
    
    #sort list by time ascending
    entry_list.sort()

    #count all entries
    count_entries = int(len(entry_list))
    
    #time of first entry
    start_time = int(entry_list[0][0])
    
    #time of last entry (abziehen from start time = running time)
    #should be 24(std) * 60(min) * 60(sec)
    last_time = int(entry_list[count_entries - 1][0])
    
    #time for search interval
    time_next_interval_starts = int(start_time + time_interval)
    
    #initial interval
    counting_hour = int(0)
    
    #loop list for counting
    i = 0
    while i < count_entries:
        #search for word and count occurences
        if entry_list[i][2].find("slut") != -1:
            count_slut = count_slut + 1
        if entry_list[i][2].find("rape") != -1:
            count_rape = count_rape + 1
        if entry_list[i][2].find("whore") != -1:
            count_whore = count_whore + 1
            
        #if time of post is greater than check-time
        if int(entry_list[i][0]) > time_next_interval_starts:
            #redefine check-time
            time_next_interval_starts = time_next_interval_starts + time_interval
            
            #append array-entry
            slut_arr.insert(counting_hour,count_slut)
            rape_arr.insert(counting_hour,count_rape)
            whore_arr.insert(counting_hour,count_whore)
            
            #reset counter
            count_slut = int(0)
            count_rape = int(0)
            count_whore = int(0)
            
            #start next interval
            counting_hour = counting_hour + 1
        
        #append array-entry after last entry
        if i == count_entries - 1:
            slut_arr.insert(counting_hour + 1,count_slut)
            rape_arr.insert(counting_hour,count_rape)
            whore_arr.insert(counting_hour,count_whore)
            
        #increase counter
        i = i + 1
    
    #count arrays
    count_entries_slut = int(len(slut_arr))
    count_entries_rape = int(len(rape_arr))
    count_entries_whore = int(len(whore_arr))
        
    #open target_file
    t = open(target_file, 'w')
    
    #insert header
    header_string = ('"hour","slut","rape","whore"\n')
    t.write(header_string)
    
    #if arrays have the same length
    j = 0
    if count_entries_slut == count_entries_rape == count_entries_whore:
        while j < count_entries_slut:
            #create insert string
            insert_string = ('"' + str(j) + '","' + str(slut_arr[j]) + '","' + str(rape_arr[j]) + '","' + str(whore_arr[j]) + '"\n')            
            
            #save string
            t.write(insert_string)
        
            #increase counter
            j = j + 1

    #close file
    t.close()
    
process_data('Comments_compiled.txt','analysis_result.csv', 3600)
