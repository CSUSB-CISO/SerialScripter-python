#!/bin/bash
if [ "$EUID" -ne 0 ]; then
        echo 'script requires root privileges'
        exit 1
fi
interface=$(ip addr show | grep "[1-9]" | grep -v "link/ether" | grep -v "inet6" | grep "state UP" | awk {'print $2'} | sed 's/://')
manager_detection(){
        if [ $(command -v apt) ]; then
                apt update
                for i in docker.io docker-compose-plugin containerd.io; do apt install -y $i; done
                systemctl start docker
        elif [ $(command -v yum) ]; then
                yum-config-manager --enable repository extras
                yum update -y
                yum upgrade -y
                yum install docker-ce -y
                systemctl enable docker
                systemctl start docker
                sleep 5
        elif [ $(command -v pacman) ]; then
                pacman -Sy
		pacman -S docker -y
                dockerd &
        elif [ $(command -v apk) ]; then
                sed -i '/community/s/^#//g' /etc/apk/repositories
		apk update 
		apk add docker openrc
		addgroup username docker
                rc-update add docker boot
                service docker start
		echo "waiting for docker service to start"
		sleep 5
        fi
}
container_install(){
	echo 'Installing Snort container for you, pumpkin <3'
	docker pull l3m0n42/snockerv4:latest
	docker run -td --name snocker --rm --net=host --read-only=true l3m0n42/snockerv4
        ls
        sleep 5
        docker exec snocker snort -Q -c /usr/local/snort.lua -R snort3.rules -i $interface --daq=afpacket --daq-mode=inline
}
manager_detection
container_install
