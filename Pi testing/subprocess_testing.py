import subprocess
import time

host = "FEMTAsimboxPi.local"
user = "pi"

def ssh_test(cmd):
    arg = f"ssh {user}@{host} \"{cmd}\""
    print(arg)
    sp = subprocess.run(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"command: {cmd} \n\nstdout: {sp.stdout.decode()} \n\nstderr: {sp.stderr.decode()}")

#ssh_test("cd 'FEMTAFYESIMBOXsoftware; ls")

def comms_test():
    arg1 = f"ssh {user}@{host} \"cd \\\"FEMTAFYESIMBOXsoftware/Pi testing\\\"; python ssh_leds.py\""
    print(arg1)
    sp1 = subprocess.Popen(arg1,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    arg2 = f"ssh {user}@{host} \"cd \\\"FEMTAFYESIMBOXsoftware/Pi testing\\\"; echo \\\"1\\\" > state\"" #https://xkcd.com/1638/
    print(arg2)
    sp2 = subprocess.run(arg2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
    sp1.wait(10)
    print(f"stdout: {sp1.stdout.read().decode()} \nstderr: {sp1.stderr.read().decode()}")
    print(f"stdout: {sp2.stdout.decode()} \nstderr: {sp2.stderr.decode()}")
    assert sp1.poll() is None
    arg3 = f"ssh {user}@{host} \"cd \\\"FEMTAFYESIMBOXsoftware/Pi testing\\\"; rm state; touch state"
    sp3 = subprocess.run(arg3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)

comms_test()