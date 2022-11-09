import matplotlib.pyplot as plt

def fib(x):
    # This function returns all the fibonacci numbers up to x
    if x < 1: return None

    ret = [0,1]
    while ret[-1] < x:
        ret.append(ret[-1] + ret[-2])
    return ret 
    
    
if __name__ == "__main__":
    _fib = fib(548879)
    print(_fib)

    import numpy as np
    dual_fib = np.fft.rfft(_fib)
    print(len(dual_fib))
    

    
 
