# Work-in-progress, purpose built logger for diagnostics and recording
# during simbox experiments.

class Logger:
    
    instances = 0
    file_objects = dict()

    # Generator for unique instance IDs
    @staticmethod
    def __id_gen():
        next_id = 0
        while True:
            yield next_id
            next_id += 1
    __id = __id_gen.__func__()  # Build generator object from function

    def __init__(self):
        print("in __init__")

    def __enter__(self):
        print("in __enter__")
        # Members of self.__class__ provides implementation of "static" members--shared between all instances of this class
        self.id = next(self.__class__.__id)
        self.__class__.instances += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__class__.instances -= 1
        if not self.__class__.instances:    # No more active instances remaining, i.e. we're last to be shut down
            for fo in self.__class__.file_objects.values():
                fo.close()
        return None

    def write(self, text, filename, _print=False) -> None:
        if filename not in self.__class__.file_objects.keys():
            self.__class__.file_objects[filename] = open(filename, "a")
        
        self.__class__.file_objects[filename].write(text)

        if _print:
            print(text)


if __name__ == '__main__':
    with Logger() as log1, Logger() as log2:
        print(log1.id, log2.id)