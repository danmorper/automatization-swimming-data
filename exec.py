import os
import time 
script_files = ['link.py', 'demo.py', 'pdf_csv.py', 'merge_csv.py']
#create file time.txt
with open('time.txt', 'w') as f:
    pass

for script in script_files:
    # start time counter
    start_time = time.time()
    with open(script, 'r') as file:
        script_content = file.read()
        exec(script_content)
    # end time counter
    end_time = time.time()
    # save time in time.txt file
    with open('time.txt', 'a') as f:
        f.write(script + ' took ' + str(end_time - start_time) + ' seconds\n')
        f.write('-----------------------------------\n')