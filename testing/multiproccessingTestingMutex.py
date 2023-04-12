import multiprocessing
from multiprocessing import Lock, Process, current_process, Value, Array
from ctypes import c_double, c_char_p
import time

def runHouseAPI(sharedsum, somestring):
    while True:
        if sharedsum.value >= 100:
            break
        name = current_process().name
        print(f"sum in now {sharedsum.value} {name} adds 1, previous user {somestring.value}")
        sharedsum.value += 1
        somestring.value = bytes(current_process().name, encoding="utf-8")
        time.sleep(0.1)

#typecode_to_type = {
#    'c': ctypes.c_char,     'u': ctypes.c_wchar,
#    'b': ctypes.c_byte,     'B': ctypes.c_ubyte,
#    'h': ctypes.c_short,    'H': ctypes.c_ushort,
#    'i': ctypes.c_int,      'I': ctypes.c_uint,
#    'l': ctypes.c_long,     'L': ctypes.c_ulong,
#    'q': ctypes.c_longlong, 'Q': ctypes.c_ulonglong,
#    'f': ctypes.c_float,    'd': ctypes.c_double
#    }

if __name__ == '__main__':
    nr_of_proccess = 10
    processes = []
    lock = Lock()
    sharedsum = Value('i', 0, lock=lock)
    somestring = Array('c', 256, lock=lock) #256 is length of array
    # x = Value(c_double, 0, lock=lock)
    # s = Array('c', b'hello world', lock=lock)
    # A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)
    for w in range(nr_of_proccess):
        p = Process(target=runHouseAPI, args=(sharedsum, somestring))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
