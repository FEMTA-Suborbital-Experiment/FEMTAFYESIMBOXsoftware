import subprocess

host = "FEMTAsimboxPi.local"
user = "pi"
#password = "FEMTAsoftwareFYEraspberryPI2020."
command = "cd Project_Files; ls"

args = f"ssh {user}@{host} '{command}'".split()

sp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(f"stdout: {sp.stdout.decode()} \n\nstderr: {sp.stderr.decode()}")