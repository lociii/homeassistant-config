# install ubuntu server with base system and ssh server
# my user is called "jens", adjust to your own needs

# allow sudo for user
$(ship) adduser $USER sudoers

# fix locales
$(ship) export LANGUAGE=en_US.UTF-8
$(ship) export LANG=en_US.UTF-8
$(ship) export LC_ALL=en_US.UTF-8
$(ship) sudo locale-gen en_US.UTF-8
$(ship) sudo dpkg-reconfigure locales

# update
$(ship) sudo apt update
$(ship) sudo apt upgrade

# copy ssh public key over and add to authorized keys
$(ship) mkdir ~/.ssh
$(local) scp ~/.ssh/id_rsa.pub jens@10.211.112.10:/home/jens/.ssh/authorized_keys

# copy ship's ssh key over
$(local) scp ~/ship-ssh/id_rsa jens@10.211.112.10:/home/jens/.ssh/id_rsa
$(local) scp ~/ship-ssh/id_rsa.pub jens@10.211.112.10:/home/jens/.ssh/id_rsa.pub

# edit /etc/ssh/sshd_config
# disable root login (PermitRootLogin no)
# disable password login (PasswordAuthentication no)
# enable public key login (PubkeyAuthentication yes)

# install docker
$(ship) sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common
$(ship) curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
$(ship) sudo apt-key fingerprint 0EBFCD88
$(ship) sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
$(ship) sudo apt update
$(ship) sudo apt install docker-ce

# manage docker as non root
$(ship) sudo groupadd docker
$(ship) sudo usermod -aG docker $USER
# log out and back in to re-evaluate groups

# test docker setup
$(ship) docker run hello-world

# make docker start at boot
$(ship) sudo systemctl enable docker

# install compose as docker container (see https://github.com/docker/compose/releases for latest version)
$(ship) sudo curl -L --fail https://github.com/docker/compose/releases/download/1.22.0/run.sh -o /usr/local/bin/docker-compose
$(ship) sudo chmod +x /usr/local/bin/docker-compose

# clone home assistant config repo
git clone git@github.com:lociii/homeassistant-config.git ~/homeassistant

# generate diffie helman cipher
$(ship) openssl dhparam 2048 -out ~/homeassistant/nginx/cert/dhparam.pem

# fill .env and homeassistant/secrets.yaml with their respective content

# create letsencrypt/domains.txt and add the domains you want to generate certificates for

# create influxdb
$(ship) docker-compose exec influxdb influx
$(influxdb) CREATE DATABASE home_assistant

# firetv - generate adb key used to connect
$(ship) docker-compose run homeassistant bash
$(homeassistant) apt install adb
$(homeassistant) adb start-server
$(homeassistant) adb connect <firetv>  # confirm connection on firetv (tick always allow), repeat for each firetv
$(homeassistant) cp ~/.android/adbkey* /config/firetv
