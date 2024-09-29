class LinearFunction:
    def __init__(self, m, c, a):
        self.m = m
        self.c = c
        self.a = a

    def __call__(self, x):
        return self.m * (x+self.a) + self.c

    def __str__(self):
        return f"{self.m}(x+{self.a}) + {self.c}"

    def __repr__(self):
        return self.__str__()