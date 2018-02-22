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

def ow(r):
    for i in r:
        if len(r)>4:
            return 0

def oii(a):
    try:
        for i in a:
            print(3)

        with open('myfile.txt', 'r') as f:
            print(33)
            for i in a:
                continue
                print(3)
                if f:
                    f.read()
                    if f:
                        f.read()
                    else:
                        return 0
                else:
                    return 0
                    raise
                    if f:
                        f.read()
                    else:
                        raise
    except ValueError:
        print ("x")
    except IOError as e:
        print ("y")
    finally:
        f = 9
def puts(i):
    for j in i:
        for j in i:
            if i:
                return 0
                print(k)
            else:
                i = 4
        else:
            print(3)

