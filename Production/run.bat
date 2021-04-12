@ECHO OFF
scp config.txt pi@FEMTAsimboxPi.local:FEMTAFYESIMBOXsoftware/simbox
ssh pi@FEMTAsimboxPi.local "activate; python3.8 -m ~/FEMTAFYESIMBOXsoftware/simbox"
