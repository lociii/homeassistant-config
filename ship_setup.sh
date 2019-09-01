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

# install snap package manager
$(ship) sudo apt install snapd

# install docker
$(ship) sudo snap install docker
$(ship) sudo addgroup --system docker
$(ship) sudo adduser $USER docker
$(ship) newgrp docker

# restart docker
$(ship) sudo snap disable docker
$(ship) sudo snap enable docker

# test docker setup
$(ship) docker run hello-world

# clone home assistant config repo
git clone git@github.com:lociii/homeassistant-config.git ~/homeassistant

# fill .env and homeassistant/secrets.yaml with their respective content

# create letsencrypt/domains.txt and add the domains you want to generate certificates for

# create influxdb
$(ship) docker-compose run --rm influxdb influx
$(influxdb) CREATE DATABASE home_assistant

# firetv - generate adb key used to connect
# can be done using docker-compose run since the package doesn't need to be persintent on image
$(ship) docker-compose run --rm homeassistant bash
$(homeassistant) apt install adb
$(homeassistant) adb start-server
$(homeassistant) adb connect <firetv>  # confirm connection on firetv (tick always allow), repeat for each firetv
$(homeassistant) cp ~/.android/adbkey* /config/firetv
