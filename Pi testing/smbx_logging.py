# Work-in-progress, purpose built logger for diagnostics and recording
# during simbox experiments.

class Logger:
    
    instances = 0
    file_objects = dict()

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        Logger.instances += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger.instances -= 1
        if not Logger.instances:    # No more active instances remaining, i.e. we're last to be shut down
            for fo in Logger.file_objects.values():
                fo.close()
        return None

    def write(self, text, filename, _print=False):
        if filename not in Logger.file_objects.keys():
            # open with mode x because we neither want to overwrite a previous log nor combine two logs together
            try:
                Logger.file_objects[filename] = open(filename, "x", encoding="ascii")
            except FileExistsError as e:
                raise Exception(f"log file \"{filename}\" already exists") from e 
        
        Logger.file_objects[filename].write(self.name + ": " + text + "\n")

        if _print:
            # Print logged message to terminal. These should be infrequent and
            # straightforward, so no need to incluse the logger name
            print(text)


if __name__ == '__main__':
    with Logger("main") as log1, Logger("arduino") as log2:
        print(log1.name, log2.name)
        log1.write("Hello World!", "test.txt")
        log2.write("Hello again", "test.txt", _print=True)
