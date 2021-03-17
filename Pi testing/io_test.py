import io
import time

def run(amount, iterations=100, buffering=-1):
	f = open("test.txt", "w", encoding="ascii",  buffering=buffering)
	start = time.perf_counter()
	for _ in range(iterations):
		f.write("P"*(amount - 1) + "\n")
	f.close()
	print(f"Total time: {1000 * (time.perf_counter() - start)} ms (for {iterations} x {amount} bytes with buffering = {buffering})")

def sio(amount, iterations=100, buffering=-1):
	stringio = io.StringIO()
	start = time.perf_counter()
	for _ in range(iterations):
		stringio.write("P"*(amount - 1) + "\n")
	with open("test.txt", "w") as f:
		f.write(stringio.getvalue())
	print(f"Total time:  {1000 * (time.perf_counter() - start)} ms (for {iterations} x {amount} bytes with StringIO")

if __name__ == "__main__":
	import sys
	run(*map(int, sys.argv[1:]))
	sio(*map(int, sys.argv[1:]))

