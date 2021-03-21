@ECHO OFF
scp config.txt pi@FEMTAsimboxPi.local:Project_Files/Production
ssh pi@FEMTAsimboxPi.local "activate; cd Project_Files/Production; python3.8 main.py debug"
