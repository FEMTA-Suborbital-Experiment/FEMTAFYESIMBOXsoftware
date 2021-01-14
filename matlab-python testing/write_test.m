% Test to see how quickly Matlab can write data to an external file.
% This info is no longer needed (see header in read_timing.py)

tic
data = rand(15);
data = round(data * 1000, 4);
writematrix(data, 'sample_data.csv');
toc
