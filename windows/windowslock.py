import win32con, win32file, pywintypes

LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK  
LOCK_SH = 0 # The default value  
LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY  
__overlapped = pywintypes.OVERLAPPED(  )  

def lock(file, flags):  
    hfile = win32file._get_osfhandle(file.fileno(  ))  
    win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)  

def unlock(file):  
    hfile = win32file._get_osfhandle(file.fileno(  ))  
    win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)  

f = open('test.jpg')
lock(f, LOCK_EX)  
f.write(msg + "\n")  
unlock(f)  