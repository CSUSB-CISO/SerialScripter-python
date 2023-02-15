How can we find all hosts running ssh?
SELECT * FROM hosts JOIN services ON hosts.id = services.host_id WHERE services.port = 22;

How can we get all shares on the C:/ drive?
SELECT * FROM hosts JOIN shares ON hosts.id = shares.host_id WHERE shares.fullpath LIKE '%C:/%';

How can we find all hosts on the 192.168.1 subnet?
SELECT * FROM hosts WHERE hosts.ip LIKE '192.168.1%';

Find all hosts that have a netcat task running?
SELECT * FROM hosts JOIN tasks ON hosts.id = tasks.host_id WHERE tasks.name = 'nc' OR tasks.name = 'nc.exe';

Find all docker containers runnign on host 169?
SELECT * FROM docker JOIN hosts on hosts.id = docker.host_id WHERE hosts.name = 'host-169';
