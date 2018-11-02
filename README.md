# My HomeAssistant setup

Hi, I'm Jens and this is how I set up my home automation using HomeAssistant.
One of the main targets is to use devices which don't rely on cloud services wherever possible.

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

### Zigbee

Running [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt) on a Raspberry Pi 3 Model B using a [GBAN CC2530](http://www.gban.cn/en/product_show.asp?id=43) zigbee sniffer.

## Ecosystem

### Lights

* digitalSTROM
* Trådfri via Hue bridge (to be migrated to zigbee2mqtt)

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
* Xiaomi Aqara window/door sensors
* Xiaomi Aqara climate sensors
* Xiaomi MiFlora plant sensors (via [ESP32 BLE gateway](https://github.com/sidddy/flora))

### Power plugs

* TP Link HS110 power plugs
* OSRAM smart+ plugs

### Misc

* Samsung Printer CLX-4190 Series

### Planned ecosystem

* Xiaomi vacuum gen2 (arrived, to be integrated)
* Xiaomi Aqara magic cube (arrived, not working with zigbee2mqtt right now, [source](https://github.com/Koenkk/zigbee2mqtt/issues/498))
