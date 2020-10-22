fp = 'sample_data.csv';
load hat.m %High-accuracy timer that I don't know how to use

data = rand(15);
data = round(data * 1000, 4);
time = hat;
fid = fopen(fp, 'w');
fprintf(fid, data);
fclose(fid);
diff = hat - time;
fprintf(diff);