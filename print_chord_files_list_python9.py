# import os
# from datetime import timedelta

# # files = 
# # ftype = 
# Dirname = os.path.dirname

# def read_dir(directory): 
# 	print("Directory: " + str(os._getitem Dirname(str(directories)+"/"+''.join([file for file in files if ftype != 'D']))[0])) 
# 	directories = os.listdir('.')
	
#     for dir_entry, filename in zip(*enumerate(os._getitemDirname(str(directories)+"/"+''.join([file for file in files if ftype != 'D']))): 
#         print('Directory:', str((dirEntry.baseName() + '/')[:-4])) dir\_entry = os._cachedirpath(\*os.*) [fname=str(filename)] 

import os
import re

def read_dir(directory):
    # List all files and directories in the specified directory
    entries = os.listdir(directory)

    for entry in entries:
        entry_path = os.path.join(directory, entry)

        if os.path.isdir(entry_path):
            # If it's a directory, print its name and call the function recursively
            # print('Directory:', entry)
            read_dir(entry_path)

            # find the Direcory likes '01 - Eb Major' using 're' module
            # and if it have hyphen twice like '04 - Eb Major - C Minor', or '10 - A Major - F# Minor' skip them
            if re.search(r'^\d{2}\s-\s[A-G][b#]?\s(Major|Minor)$', entry):
                print('Subdirectory:', entry)
            elif re.search(r'^\d{2}\s-\s[A-G][b#]?\s[Mm]ajor\s-\s[A-G][b#]?\s[Mm]inor$', entry):
                print('Directory:', entry)
            else:
                print('Unknown:', entry)

            
        elif os.path.isfile(entry_path):
            # 01
            # If it's a file, print its name
            # print('File:', entry)

            # 02
            # remove the .txt extension
            # print('File:', entry[:-4])

            # split the filename into a list of words
            words = re.split(r'[\s\-\_]+', entry[:-4])
            # print(words)

            # 03
            
            # 04
            # make a dictionary of words, with [0] as the key and [1] as the value
            # words_dict = {words[0]: words[1]}
            # print(words_dict)
        else:
            # It's neither a file nor a directory
            print('Unknown:', entry)

# Example usage:
read_dir('/Users/mac/git/privateGPT/source_documents')
