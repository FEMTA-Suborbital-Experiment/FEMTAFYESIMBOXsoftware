import time
import numpy as np
import tqdm
from math import exp

tests = 1000
desired_delay = 10e-3

one_over_e = 1 / exp(1)

def antsySleep(time_s, percentage=0.001, resolution=1e-4):
    target_time = time.perf_counter() + time_s
    acceptable_remaining = percentage * time_s

    remaining = target_time - time.perf_counter()
    # Sleep exponentially until we hit the "limit" to which sleep is "reliable"
    while remaining * 0.5 > resolution:
        time.sleep(remaining * 0.5)
        remaining = target_time - time.perf_counter()

    # Busywait for the remaining amount
    while remaining > acceptable_remaining:
        remaining = target_time - time.perf_counter()

if __name__ == "__main__":
    times = np.zeros((3, tests))

    print(f"Running timing test using a sleep time of {desired_delay}...")
    for i in tqdm.trange(tests):
        times[0,i] = time.perf_counter()
        # time.sleep(desired_delay)
        antsySleep(desired_delay) # Much better for small delays
        times[1,i] = time.perf_counter()
            
    print("Test complete.")
    times[2] = times[1] - times[0]
    spacings = np.diff(times[0])

    print(f"Sleep times for delay of {desired_delay}s: (min|avg|max) {np.min(times[2]):0.3e}s | {np.mean(times[2]):0.3e}s | {np.max(times[2]):0.3e}s")
    print(f"Sleep times for delay of {desired_delay}s as %: (min|avg|max) {np.min(times[2])/desired_delay:0.3%} | {np.mean(times[2])/desired_delay:0.3%} | {np.max(times[2])/desired_delay:0.3%}")
    print(f"Delays between loops [s]: (min|avg|max) {np.min(spacings):0.3e}s | {np.mean(spacings):0.3e}s | {np.max(spacings):0.3e}s")
