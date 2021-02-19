@ECHO OFF
scp config.txt pi@FEMTAsimboxPi.local:Project_Files/Production
ssh pi@FEMTAsimboxPi.local "cd Project_Files/Production; python main.py"