import subprocess

host = "FEMTAsimboxPi.local"
user = "pi"
password = "FEMTAsoftwareFYEraspberryPI2020."
command = "\"echo 'Hello World!'\""

arg = f"echo {password} | ssh {user}@{host} {command}" #echo {password} | ssh {user}@{host} {command}
print(arg)

stdout, stderr = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()