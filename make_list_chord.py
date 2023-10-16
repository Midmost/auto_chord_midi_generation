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

def read_dir(directory):
    # List all files and directories in the specified directory
    entries = os.listdir(directory)

    for entry in entries:
        entry_path = os.path.join(directory, entry)

        if os.path.isdir(entry_path):
            # If it's a directory, print its name and call the function recursively
            print('Directory:', entry)
            read_dir(entry_path)
        elif os.path.isfile(entry_path):
            # If it's a file, print its name
            print('File:', entry)
        else:
            # It's neither a file nor a directory
            print('Unknown:', entry)

# Example usage:
read_dir('/Users/mac/git/privateGPT/source_documents')
