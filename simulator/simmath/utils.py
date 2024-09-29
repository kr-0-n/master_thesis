import matplotlib.pyplot as plt
from LinearFunction import LinearFunction

def plot(*functions : LinearFunction):
    for f in functions:
        x = range(0, 10)
        y = [f(i) for i in x]
        plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Linear Functions")
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    
    plt.legend([str(f) for f in functions])
    plt.show()