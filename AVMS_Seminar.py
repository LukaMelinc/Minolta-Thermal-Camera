import time
import threading

import fluke
import cyclops
import GUI

# Thread function to parallel measure values
def RepeatFunction(interval, function, *args, **kwargs):
    threading.Timer(interval, RepeatFunction, [interval, function] + list(args), kwargs).start()
    function(*args, **kwargs)

def Measure():
    print("Function is called")


if __name__ == "__main__":

    # Declare classes #
    fluke = fluke.Fluke()
    cyclops = cyclops.Cyclops()
    gui = GUI.StartWindow()
    
    #cyclops.CyclopsStatusRead()

    # Call my_function every n seconds
    #RepeatFunction(1, Measure)


        
    
