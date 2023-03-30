if [ "$EUID" -ne 0 ]; then
        echo 'script requires root privileges'
        exit 1
fi
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
    mkdir -p /var/log/rsyslog
    docker pull l3m0n42/jeffery-dahcker:latest 
    docker run -it --name jeffery-dahcker --net=host --mount type=bind,source=/var/log/rsyslog,target=/var/log/rsyslog l3m0n42/jeffery-dahcker

}

manager_detection
container_install
