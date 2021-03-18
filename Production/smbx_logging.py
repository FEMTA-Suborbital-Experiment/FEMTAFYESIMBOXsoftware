# Purpose built logger for diagnostics and recording during simbox experiments.
# Works with context managers. If not using context managers, call start()
# (right) before using and close() when done.

import time

class Logger:
    
    instances = 0
    file_objects = dict()

    def __init__(self, name):
        self.name = name
        self.start_t = None

    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return None


    def start(self):
        Logger.instances += 1
        self.start_t = time.perf_counter()

    def close(self):
        Logger.instances -= 1
        if not Logger.instances: # No more active instances remaining, i.e. we're last to be shut down
            for fo in Logger.file_objects.values():
                fo.close()


    def write(self, text, filename, _print=False):
        assert self.start_t is not None, f"Logger \"{self.name}\" has not had \"start()\" called"

        if filename not in Logger.file_objects.keys():
            # open with mode x because we neither want to overwrite a previous log nor combine two logs together
            try:
                Logger.file_objects[filename] = open(filename, "x", encoding="ascii")
            except FileExistsError as e:
                raise Exception(f"log file \"{filename}\" already exists") from e 
        
        Logger.file_objects[filename].write(f"{self.name} [{time.perf_counter() - self.start_t}]: {text}\n")

        if _print:
            # Print logged message to terminal. These should be infrequent and
            # straightforward, so no need to include the logger name
            print(text)


if __name__ == '__main__':
    with Logger("main") as log1, Logger("arduino") as log2:
        print(log1.name, log2.name)
        log1.write("Hello World!", "test.txt")
        log2.write("Hello again", "test.txt", _print=True)
