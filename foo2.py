'''def zap():
    o = True
    if o:
        try:
            a = 10 / 0
        except ZeroDivisionError:
            print("Oops, invalid.")
        except BaseException:
            while a in o:
                print 121
        except ImportError:
            while a in o:
                print 121
        else:
            # Exception didn't occur, we're good.
            pass
        finally:
             return 0
def i():
    try:
        # Division by zero raises an exception
        10 / 0
    except ZeroDivisionError:
        print("Oops, invalid.")
    except ImportError:
        print("Oops, invalid.")
    else:
        # Exception didn't occur, we're good.
        pass
    finally:
        # This is executed after the code block is run
        # and all exceptions have been handled, even
        # if a new exception is raised while handling.
        print("We're done with that.")

def foo(a):
    a = 3
    b = 4
    if(a<b):
        for i in range(0,5):
            b+=4
            print 'oi'
            continue
            for k in range(0,4):
                print 'dub'
                for o in range(0,3):
                    a = 4
                    c = True
                    if (a < b):
                        a = b
                        if (a < b):
                            a = b
                            if (a < b):
                                a = b
                            else:
                                a = b
                        elif(x>1):
                            a = b
                            if (a < b):
                                a = b
        else:
            print 'wauhwuahw'

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
       passnum = passnum-1 '''