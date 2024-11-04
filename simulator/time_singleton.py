class TimeSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeSingleton, cls).__new__(cls)
            cls._instance.time = 0
        return cls._instance

    def tick(self):
        self.time += 1

    def getTime(self):
        return self.time