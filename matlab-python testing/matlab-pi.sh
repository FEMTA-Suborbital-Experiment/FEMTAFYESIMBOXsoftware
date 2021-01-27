# Shell script to run a python script and a Matlab executable concurrently.
# Currently set up to run a sockets test.

cd /home/pi/MATLAB_ws/R2020b
python '/home/pi/Project_Files/matlab-python testing/pi_matlab_socket.py' & 
./python_matlab_sockets.elf && 
fgp