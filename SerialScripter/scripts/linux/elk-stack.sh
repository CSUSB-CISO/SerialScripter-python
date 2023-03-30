#!/bin/bash

# TODO:
	# 1. Configure installation for client-side integrations (may not be necessary since we can make POST requests to send our own data manually, unless we want to also monitor log files but we may also be able to make POST requests for these too 

# add_kubernetes_metadata
# hosts

function cmdExist() {
	command -v "$1" >/dev/null 2>&1
}

function dropPipelineConfig() {
	cat <<EOF >/root/logstash.config
input {
  http {
    port => 8080
    codec => "json"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "my-index-%{+YYYY.MM.dd}"
  }
  stdout {
    codec => rubydebug
  }
}
EOF
}

function dropDockerCompose() {
	echo "Dropping docker compose file..."
	cat <<EOF >/root/dockercompose.yml
services:
  webinter:
    image: docker.elastic.co/kibana/kibana:8.6.2
    container_name: kibana
    ports: 
      - "5601:5601"
  
  db:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.6.2
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - d=false
    ports:
      - "9200:9200"
      - "9300:9300"
  authentication:
    image: docker.elastic.co/logstash/logstash:8.6.2
    container_name: logstash
    volumes:
      - /root/logstash.config:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "8080:8080"
EOF
}

function checkcURL() {
	if [ -x "$(command -v curl)" ]; then
		echo "cURL is already installed"
	fi

	# Install cURL
	if [ -x "$(command -v apt-get)" ]; then
  		sudo apt-get update
  		sudo apt-get install -y curl
	elif [ -x "$(command -v yum)" ]; then
  		sudo yum install -y curl
	elif [ -x "$(command -v pacman)" ]; then
  		sudo pacman -Syu curl
	elif [ -x "$(command -v apk)" ]; then
  		sudo apk update
  		sudo apk add curl
	else
  		echo "Unable to install cURL: package manager not found"
  		exit 1
	fi

}

installType=$1
elkServerIP=$2

### NOTE: INSTALLATION FOR ELASTICSEARCH INTEGRATIONS SUCH AS LOG FILES WILL ONLY WORK FOR CERTAIN LINUX DISTROS
function configFileBeatClient() {
	# Install filebeat on respective distro
	#checkcURL
	#echo "Installing filebeat..."
	#curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.2-amd64.deb
	#sudo dpkg -i filebeat-8.6.2-amd64.deb

	# Setup filebeat config
	echo "Configuring filebeat..."
	#sudo sed -i "s/#hosts:/hosts: [\"$elkServerIP:5044\"]/" /etc/filebeat/filebeat.yml
    # Change reload.enabled: false to true
	sudo sed -i 's/reload.enabled: false/reload.enabled: true/' /etc/filebeat/filebeat.yml
	# change setup.dashboards.enabled: false to true
    sudo sed -i 's/#setup.dashboards.enabled: false/setup.dashboards.enabled: true/' /etc/filebeat/filebeat.yml
	# Change IP addrs
	#sudo sed -i 's/host: "localhost:5601"/host: "${elkServerIP}:5601"/' /etc/filebeat/filebeat.yml
	#sudo sed -i 's/hosts: \["localhost:9200"\]/hosts: \[\"${elkServerIP}:9200\"]/' /etc/filebeat/filebeat.yml
	

	sudo sed -i "s/#host: \"localhost:5601\"/host: \"${elkServerIP}:5601\"/g" /etc/filebeat/filebeat.yml # Current problem is it isn't uncommenting this, but it does change the IP addr
	sudo sed -i "s/hosts: \[\"localhost:9200\"\]/hosts: \[\"${elkServerIP}:9200\"\]/g" /etc/filebeat/filebeat.yml # Current problem is it isn't changing the IP from localhost
	# Start and enable Filebeat ser```vice
	echo "Enabling filebeat service..."
    if command -v systemctl >/dev/null 2>&1; then
        # Use systemctl to start and enable service on systemd-based systems
        sudo systemctl start filebeat
        sudo systemctl enable filebeat
    elif command -v service >/dev/null 2>&1; then
        # Use service to start and enable service on SysV-init systems
        sudo service filebeat start
        sudo chkconfig filebeat on
    else
        echo "Unable to start and enable Filebeat service"
        return 1
    fi
	
	# enable system module
	sudo filebeat modules enable system
	echo "Filebeat should now be configured!"

	# Now we must modify the contents of the module config file you previously enabled
	sed -i 's/enabled: false/enabled: true/g' /etc/filebeat/modules.d/system.yml
	sed -i 's/#var.paths:/var.paths: ["\/var\/log\/*.log"]/g' /etc/filebeat/modules.d/system.yml

	sudo filebeat setup


}

function installFileBeat() {
	checkcURL
	if [ "$packageManager" == "dpkg" ]; then
		# install it the dpkg way
		curl -L -O --insecure https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.2-amd64.deb
		sudo dpkg -i filebeat-8.6.2-amd64.deb
	elif [ "$packageManager" == "rpm" ]; then
		# install it the rpm way
		curl -L -O --insecure https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.2-x86_64.rpm
		sudo rpm -vi filebeat-8.6.2-x86_64.rpm
	fi
} 

function checkRoot() {
	if [ "$(id -u)" -eq 0 ]; then
		echo "Running as root! Continuing"
	else
		echo "Not running as root!"
		exit 1
	fi
}

function checkPackageManager() {
	if [ -x "$(command -v dpkg)" ]; then
		echo "DPKG in use!"
		packageManager="dpkg"
	elif [ -x "$(command -v rpm)" ]; then
		echo "RPM in use!"
		packageManager="rpm"
	else
		echo "Unknown package manager in use! Cannot continue with installation!"
		exit 1
	fi
}

function configFileBeatServer() {
	#checkcURL
	#echo "Installing filebeat..."
	#curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.2-amd64.deb
	#sudo dpkg -i filebeat-8.6.2-amd64.deb
	echo "Configuring filebeat log file...."
	sed -i 's/reload\.enabled: false/reload.enabled: true/g' /etc/filebeat/filebeat.yml
	echo "Enabling filebeat..."
	systemctl start filebeat
	filebeat modules enable elasticsearch
	filebeat modules enable kibana
	filebeat modules enable system
}



function checkArgs() {
	
	checkPackageManager
	if [ -z "$installType" ]; then
		echo "No installation type chosen!"
	else
		checkRoot
		installFileBeat
		# Call function based on installation type
		if [ "$installType" == "server" ]; then
			echo "Server installation!"
			# Check if docker-compose is installed
			if ! cmdExist "docker-compose"; then
				echo "Installing docker..."
				curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
				echo "Docker compose not found! Installing..."
				LATEST_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')
    			sudo curl -L --insecure "https://github.com/docker/compose/releases/download/$LATEST_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    			sudo chmod +x /usr/local/bin/docker-compose
    			echo "Docker Compose $LATEST_VERSION has been installed."
			else
				echo "Docker compose already installed! Continuing..."
			fi

			echo "Dropping docker compose file..."
			dropDockerCompose
			echo "Dropping logstash config file..."
			dropPipelineConfig
			echo "Starting docker daemon..." # USES SYSTEMCTL, MAKE IT MORE PLATFORM AGNOSTIC
			sudo systemctl start docker
			echo "Starting ELK stack..."
			sudo docker-compose -f /root/dockercompose.yml up -d 

			configFileBeatServer

		elif [ "$installType" == "client" ]; then
			echo "Client installation!"
			if [ -z "$elkServerIP" ]; then
				echo "No IP address provided for ELK server!"
			else
				echo "ELK server IP: $elkServerIP"
				configFileBeatClient
			fi
		else
			echo "Invalid installation type!"
		fi
	fi
}

checkArgs
