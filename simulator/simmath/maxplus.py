from simmath.LinearFunction import LinearFunction
def multiply(*functions: LinearFunction) -> LinearFunction:
    f_t = LinearFunction(0, 0, 0)
    for f in functions:
        f_t.m = f_t.m + f.m
        f_t.c = f_t.m * f_t.a + f.m * f.a + f_t.c + f.c 
    return f_t

def devide(f: LinearFunction , g: LinearFunction) -> LinearFunction:
    f_t = LinearFunction(0, 0, 0)
    f_t.m = f.m - g.m
    f_t.c = f.m * f.a + f.c - g.m * g.a - g.c
    return f_t