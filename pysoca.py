
#primeiro arg sao os metodos que terao os grafos gerados e o segundo testes
def hi():
    print('ooo')
    print(str(sys.argv))
    try:
        if(len(sys.argv)==3):
            imp = importlib.import_module(str(sys.argv[1]))
            print(imp)
            code = inspect.getsource(imp)
            print "koe"
            with open('foo.py', "w") as f:
                f.write(code)
            print("first")
            imp2 = importlib.import_module(str(sys.argv[2]))
            print(imp2)
            cod = inspect.getsource(imp2)
            with open('test.py', "r") as f:
                print("jjj")
                newT = f.read().replace("#[insertclass]", cod)
            with open('test.py', "w") as f:
                f.write(newT)
            import os
            os.system('python test.py')

            with open('test.py', "r") as f:
                newT = f.read().replace(cod,"#[insertclass]")
            with open('test.py', "w") as f:
                f.write(newT)
            with open('foo.py', "w") as f:
                f.write("")
    except:
        print "Wrong input or file not found"
if __name__ == '__main__':
    import sys
    import ast
    import inspect
    import importlib

    hi()
#import test
