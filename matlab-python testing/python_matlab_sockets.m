% Function testing inter-process communication on the Pi.
% This script connects to a socket opened by the Python script, sends data,
% receives data, and prints that.
% Currently, it's passing arrays of uint8s back and forth.

function python_matlab_sockets() %#codegen

t = tcpclient('127.0.0.1', 65535);
write(t, uint8([11,12,13,14,15]));
pause(0.25);
bytes = read(t);
for i = 1:5
    fprintf("Matlab received %d\n", int16(bytes(i)));
end
end