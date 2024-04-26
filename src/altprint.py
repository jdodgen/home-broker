# conditional print
import os

print_on = False
caller_name = ""
xprint = print # copy print routine

def set(printing=True, file=None):
    global print_on
    caller_name = os.path.basename(file).split(".")[0]
    print_on = printing

def print(*args, **kwargs): # replace print
    if print_on:
        xprint("["+caller_name+"]", *args, **kwargs) # the copied real print

def print_always(*args, **kwargs): # replace print
    nonlocal caller_name
    xprint("["+caller_name+"]", *args, **kwargs) # the copied real print

if __name__ == "__main__":
    from altprint import set, print
    set(printing=True, file=__file__)
    print("foo")