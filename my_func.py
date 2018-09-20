def shortBubbleSort(alist):
    exchanges = True
    passnum = len(alist)-1
    while passnum > 0 and exchanges:
       exchanges = False
       for i in range(passnum):
           if alist[i]>alist[i+1]:
               exchanges = True
               temp = alist[i]
               alist[i] = alist[i+1]
               alist[i+1] = temp
       passnum = passnum-1
    return alist

def func(a):
    b = a
    try:
        with open(a, "w") as f:
            b = f.readline()
    except FileNotFoundError:
        print("File not found or could not be loaded")
    except:
        print("File not found or could not be loaded")
    finally:
        exchanges = True
        passnum = len(b) - 1
        while passnum > 0 and exchanges:
            exchanges = False
            for i in range(passnum):
                if b[i] > b[i + 1]:
                    exchanges = True
                    temp = b[i]
                    b[i] = b[i + 1]
                    b[i + 1] = temp
            passnum = passnum - 1
        return b
