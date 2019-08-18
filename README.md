[![Travis CI build status](https://travis-ci.org/lociii/homeassistant-config.svg)](https://travis-ci.org/lociii/homeassistant-config)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

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
  access docker host system stats from the HomeAssistant container
  https://nicolargo.github.io/glances/
* traccar
  position tracking and analytics
  https://www.traccar.org/
* paperless
  document tracking and indexing
  https://github.com/the-paperless-project/paperless
* volumerize
  backup docker volumes
  https://github.com/blacklabelops/volumerize

TODO: install "notifications app" on firetv

## Custom components

### Docker Monitor

Add statistics of Docker containers as sensors and make the containers themselves available as switches.
HACS compatible fork: https://github.com/lociii/home-assistant-custom-components
Original repo: https://github.com/Sanderhuisman/home-assistant-custom-components

### digitalSTROM

Homegrown component to control my lights and shutters which are based on [digitalSTROM](https://www.digitalstrom.com/).

Check the underlying library for more details: [pydigitalstrom](https://github.com/lociii/pydigitalstrom)

### HACS

The [Home Assistant Community Store](https://hacs.netlify.com/), a project started by [@ludeeus](https://twitter.com/ludeeus) to make installing and managing non-core components much easier. Thanks from here for the great work!

HACS is used to install several other components.

## Infrastructure

### Internet connection

Internet (DSL) -> Fritz!Box 7412 (providing PPPoE passthrough) -> UniFi USG

### Network

* UniFi USG
* Ubiquiti UniFi Switch US-24 250W
* Ubiquiti UniFi AP-AC-Pro (Mainfloor)
* Ubiquiti UniFi AP (Basement)
* Ubiquiti UniFi cloud key (to manage all of the above)

### Phone

Another Fritz!Box 7412 just for VoIP connections.

Gigaset DECT base station connected to Fritz!Box and some DECT handsets.

### digitalSTROM

Light and shutter control system, see https://www.digitalstrom.com/

* dSS IP to manage the digitalSTROM installation and provide the API
* dSS 1GB as gateway to the digitalSTROM bus system, controlled by the dSS IP

### Zigbee

Running [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt) on a Raspberry Pi 3 Model B using a [GBAN CC2530](http://www.gban.cn/en/product_show.asp?id=43) zigbee sniffer.

## Ecosystem

### Lights

* digitalSTROM
* Trådfri via zigbee2mqtt

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

* UniFi presence sensor (mobile phones connected to WiFi)

### Sensors

* Darksky weather
* Waze travel time
* System sensor using glances (monitoring the docker host machine "ship")
* Xiaomi Aqara window/door sensors
* Xiaomi Aqara climate sensors
* Xiaomi Aqara water leakage sensors
* Xiaomi Aqara occopancy sensors
* Xiaomi MiFlora plant sensors (via [ESP32 BLE gateway running ESPHome](https://esphome.io/components/sensor/xiaomi_miflora.html))

### Power plugs

* TP Link HS110
* OSRAM smart+ plugs (built in zigbee router)

### Utility

* Xiaomi Roborock vacuum gen2

### Planned ecosystem

* Xiaomi Aqara magic cube
* Gosund SP111 
