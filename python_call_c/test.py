import ctypes
ll = ctypes.cdll.LoadLibrary
lib = ll('./libpycall.so')
lib.test()
