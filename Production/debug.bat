@ECHO OFF
scp config.txt pi@FEMTAsimboxPi.local:FEMTAFYESIMBOXsoftware/simbox
ssh pi@FEMTAsimboxPi.local "source ~/environments/simbox-env/bin/activate; python3.8 -m ~/FEMTAFYESIMBOXsoftware/simbox debug"
