from random import gauss

def fuzz(value, factor=0.01):
    return gauss(value, factor * value)