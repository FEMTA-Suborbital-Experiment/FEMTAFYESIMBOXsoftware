# Work-in-progress, purpose built logger for diagnostics and recording
# during simbox experiments.

class Logger:
    
    instances = 0
    file_objects = dict()

    def __enter__(self):
        self.instances += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.instances -= 1
        if not self.instances:
            for fo in self.file_objects.values():
                fo.close()
        return None

    def write(self, text, filename, _print=False):
        if filename not in self.file_objects.keys():
            self.file_objects[filename] = open(filename, "a")
        
        self.file_objects[filename].write(text)

        if _print:
            print(text)
