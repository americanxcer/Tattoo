from __future__ import print_function
import basc_py4chan
from time import *

#repeat interval
interval = int(600)

#repeat n times
last_run = time() + (144 * interval)

#text database
filename = str('Comments_compiled.txt')

#screen output
print('start: ', time())

while time() < last_run:
    #get the board we want
    board = basc_py4chan.Board('b')

    #go through threads
    threads = board.get_all_threads()

    #function to remove non ascii letters
    def remove_non_ascii_1(text):
        return ''.join(i for i in text if ord(i)<128)

    #create list with all entries
    existing_id_list = list()
    file = open(filename,"r")
    for line in file:
        temp_string = line.split('|')
        existing_id_list.append(temp_string[0])
    file.close()

    #count etries before next run
    entries_before = int(len(existing_id_list))
    
    #for counter
    x = 0
    
    #append to .txt file
    f = open(filename, 'a')
    
    #for each thread in the list of threads
    for thread in threads:
        #for each post in each thread
        for post in thread.all_posts:
            
            #if post_id not in list, append entry
            post_id1 = str(post.post_id).replace('\n',' ')
            if post_id1 not in existing_id_list:
                timestamp1 = str(post.timestamp)
                
                #removing non ascii letters
                text_comment1 = remove_non_ascii_1(post.text_comment).replace('\n',' ')
                text_comment1 = text_comment1.replace('|',' ')
                insert_string = post_id1 + '|' + timestamp1 + '|' + text_comment1 + '\n'
                str(insert_string)
                
                #extend list with new post_id
                existing_id_list.append(post_id1)
                
                #write the post in text form
                f.write(insert_string)
                
                #count posts
                x = x + 1
    #close file
    f.close()

    #screen output
    entries_after = int(len(existing_id_list))
    count_new_entries = int((entries_after) - (entries_before))
    print(count_new_entries, ' new entries')
    print('time now: ', time())
    
    #sleep before next run
    sleep(interval)
    
print('end: ', time())