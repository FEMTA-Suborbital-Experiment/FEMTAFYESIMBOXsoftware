tic
data = rand(15);
data = round(data * 1000, 4);
writematrix(data, 'sample_data.csv');
toc
