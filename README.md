# My HomeAssistant setup

Hi, I'm Jens and this is how I set up my home automation using HomeAssistant.

## HomeAssistant environment

### NUC

NUC7I5BNK with Core i5 7260U, 16GB RAM and 500GB Samsung 860 EVO M2 SSD.  
This machine is called "ship".

### Docker host installation

Running debian server with docker and compose.  
See [setup instructions](ship_setup.sh) for details

### Docker containers

Docker is currenly running the following containers, see [compose file](docker-compose.yml) for details

* mosquitto  
  MQTT broker by eclipse  
  https://mosquitto.org/
* hadockermon  
  docker monitoring for HomeAssistant  
  https://github.com/philhawthorne/ha-dockermon
* postgresql  
  database for HomeAssistant recorder component  
  https://www.postgresql.org/
* influxdb  
  time series database  
  https://www.influxdata.com/time-series-platform/influxdb/
* grafana  
  analytics for postgresql and influxdb data  
  https://grafana.com/
* chronograf  
  a frontend for influxdb data  
  https://www.influxdata.com/time-series-platform/chronograf/
* homeassistant  
  the thing it's all about  
  https://www.home-assistant.io/
* appdaemon  
  automations for HomeAssistant  
  https://appdaemon.readthedocs.io/en/stable/
* letsencrypt  
  dehydrated and lexicon to generate ssl certificates to securely access my installation  
  https://letsencrypt.org/
* nginx  
  reverse proxy in front of HomeAssistant handling all ssl needs  
  https://www.nginx.com/
* glances  
  access docker host system stats from the 
  HomeAssistant container  
  https://nicolargo.github.io/glances/

TODO: install "notifications app" on firetv

## Infrastructure

### Internet connection

Internet -> Fritz!Box 7412 (providing PPPoE passthrough) -> UniFi USG

### Network

* Ubiquiti UniFi Switch US-24 250W
* Ubiquiti UniFi AP-AC-Pro (Mainfloor)
* Ubiquiti UniFi AP (Basement)
* Ubiquiti UniFi cloud key (to manage all of the above)

### Phone

Another Fritz!Box 7412 using the existing internet connection handling VoIP connections.

Gigaset DECT base station connected to Fritz!Box and some DECT handsets.

### digitalSTROM

Light and shutter control system, see https://www.digitalstrom.com/

* dSS IP to manage the digitalSTROM installation and provide the API
* dSS 1GB as gateway to the digitalSTROM system controlled by the dSS IP

## Ecosystem

### Lights

* digitalSTROM
* Trådfri via Hue bridge

### Shutters

* digitalSTROM

### Media

* Sonos
* Some Google Home
* Some Amazon Echo
* Some FireTV
* Synology DS212j
* Logitech Harmony hub

### Presence detection

* UniFi presence sensor

### Sensors

* Weather underground
* Google travel time
* System sensor using glances

### Misc

* Samsung Printer CLX-4190 Series
* TP Link HS110 power plugs

### Planned ecosystem

* zigbee2mqtt bridge using CC2530  
  https://github.com/Koenkk/zigbee2mqtt
* Xiaomi Aqara window sensors
* Xiaomi vacuum gen2
* Xiaomi MiFlora (plant sensors)
* Xiaomi Aqara temperarur/humidity sensor
* Xiaomi Aqara magic cube
