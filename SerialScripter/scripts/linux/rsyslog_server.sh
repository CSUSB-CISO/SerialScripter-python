# !/bin/bash

var=$(systemctl is-active rsyslog)

# install and enable rsyslog
if [[ "$var" == "active" || -w /etc/rsyslog.conf ]]; then

	systemctl unmask rsyslog
	systemctl restart rsyslog
	systemctl enable rsyslog
else 
	if [ $(command -v apt-get) ]; then # Debian based
    	apt-get install rsyslog -y
		systemctl start rsyslog
		systemctl enable rsyslog
	elif [ $(command -v yum) ]; then
    	yum -y install rsyslog
		systemctl start rsyslog
		systemctl enable rsyslog
	elif [ $(command -v pacman) ]; then 
    	yes | pacman -S rsyslog
	
		systemctl start rsyslog
		systemctl enable rsyslog
	elif [ $(command -v apk) ]; then # Alpine
    	apk update
    	apk upgrade
    	apk add bash rsyslog
	elif [ $(command -v slapt-get)]; then
		slapt-get rsyslog
	
		service rsyslog start
		service rsyslog enable
	elif [$(command -v service)]; then
		service rsyslog restart
	fi
fi
echo 'module(load="imudp")' >> /etc/rsyslog.conf 
echo 'input(type="imudp" port="514")' >> /etc/rsyslog.conf
echo '$template TraditionalFormatWithPRI,"%pri-text%: %timegenerated% %fromhost-ip% %HOSTNAME% %syslogtag%%msg:::drop-last-lf%\n' >> /etc/rsyslog.conf
echo '$template RemoteLogs,"/var/log/rsyslog.log"' >> /etc/rsyslog.conf
echo 'if $msg contains "ssl_client_socket_impl.cc" then {stop}' >> /etc/rsyslog.conf
echo '*.*;kern.none ?RemoteLogs;TraditionalFormatWithPRI & ~debug' >> /etc/rsyslog.conf
echo 'stop' >> /etc/rsyslog.conf

# restart rsyslog
if [ $(command -v systemctl) ]; then
	systemctl restart rsyslog.service

elif [ $(command -v service) ]; then
	service rsyslog restart
fi