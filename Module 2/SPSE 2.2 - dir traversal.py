#!/usr/local/bin/python3
import os

''' SPSE 2-2 Directory Traversal - Create a program which can recursively traverse directories and print the file listing in a hierarchical way '''

# Recursive solution
def print_dir(dir, num):
    # I did 2 dashes per level instead of 4, just makes printing easier
    dash = '--'
    # changes the directory to your current directory + the new dir you just moved into
    os.chdir(os.path.join(os.getcwd(),os.path.basename(dir)))
    # print the dashes + the directory you're in
    print(dash*num + os.path.basename(os.getcwd()))
    # keeps track of the level
    num+=1
    for each in os.listdir():
        if os.path.isdir(each):
            # if you reach a directory, call fcn on the new directory
            print_dir(os.path.join(dir, each), num)
            # revert back up to the previous dir and continue
            os.chdir("..")
        else:
            #prints a filename
            print (dash*num + os.path.basename(each))

print_dir(".",0)
