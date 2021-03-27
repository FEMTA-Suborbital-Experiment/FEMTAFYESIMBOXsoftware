@ECHO OFF
scp config.txt pi@FEMTAsimboxPi.local:Project_Files/Production
ssh pi@FEMTAsimboxPi.local "source ~/environments/simbox-env/bin/activate; python3.8 -m ~/Project_Files/simbox debug"
