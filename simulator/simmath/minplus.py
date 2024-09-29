from simmath.LinearFunction import LinearFunction

def min(f: LinearFunction , g: LinearFunction) -> LinearFunction:
    h = LinearFunction(0, 0, 0)
    if f.m < g.m:
        h.m = f.m
    else:
        h.m = g.m
    if f.c < g.c:
        h.c = f.c
    else:
        h.c = g.c
    h.a = f.a + g.a
    return h