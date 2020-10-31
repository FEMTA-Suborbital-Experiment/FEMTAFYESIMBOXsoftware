tic

data = 33;

t = tcpip('localhost', 65535, 'NetworkRole', 'client');
fopen(t);

fwrite(t,data);

toc

% bytes = fread(t, [1, t.BytesAvailable]);
% char(bytes)
