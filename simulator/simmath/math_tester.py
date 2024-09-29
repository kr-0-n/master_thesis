from LinearFunction import LinearFunction
from maxplus import multiply
from minplus import min
from utils import plot
f = LinearFunction(1, 0, 0)
g = LinearFunction(0.5, 0, -2)

plot(f, g, min(f,g))
print(min(f, g))