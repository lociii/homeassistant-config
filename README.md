[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

# My HomeAssistant setup

Hi, I'm Jens and this is how I set up my home automation using HomeAssistant.
One of the main targets is to use devices which don't rely on cloud services wherever possible.

## HomeAssistant environment

### NUC

NUC7I5BNK with Core i5 7260U, 16GB RAM and 500GB Samsung 970 EVO Plus M2 SSD.
This machine is called "ship".

### Home Assistant environment

Running Home Assistant Supervisor on a generic Ubuntu 19.10 installation.
See [setup instructions](https://www.home-assistant.io/hassio/installation/#alternative-install-home-assistant-supervised-on-a-generic-linux-host) for details.

All additional containers are installed and managed by the Home Assistant Supervisor.
Custom repos in use:
* Stephen Beechen (Google Drive backup)
  https://github.com/sabeechen/hassio-google-drive-backup
* Kory Prince (APC UPS daemon)
  https://github.com/korylprince/hassio-apcupsd
* Nicholas Alipaz (dynamic DNS updater)
  https://github.com/nalipaz/hassio-addons
* Markus Pöschl (i.a. Valetudo mapper)
  https://github.com/Poeschl/Hassio-Addons

## Automations

100% of my automations have been migrated to the [automations editor](automations.yaml).

## Custom components - HACS

The [Home Assistant Community Store](https://hacs.xyz/), a project started by [@ludeeus](https://twitter.com/ludeeus) to make installing and managing non-core components much easier. Thank you so much for your great work!

HACS is used to install and manage my custom components, lovelace plugins and lovelace themes.
The following components are essential to my setup:

### digitalSTROM

My [homegrown component](https://github.com/lociii/homeassistant-digitalstrom) to control my lights and shutters which are based on [digitalSTROM](https://www.digitalstrom.com/).

Check out the underlying library for more details: [pydigitalstrom](https://github.com/lociii/pydigitalstrom)

### UniFi Gateway

High level health status of UniFi Security Gateway devices via UniFi Controller

### Variable

A custom Home Assistant component for declaring and setting generic variable entities dynamically.
See [my variable definitions](variables.yaml) for use cases.

### Alexa Media Player

This is a custom component to allow control of Amazon Alexa devices in Home Assistant using the unofficial Alexa API.

### zigbee2mqtt Networkmap

Custom Component for Homeassistant to show zigbee2mqtt Networkmap

## Infrastructure

### Internet connection

Internet (DSL) -> Fritz!Box 7412 (PPPoE passthrough only) -> UniFi USG

### Network

* Ubiquiti UniFi USG
* Ubiquiti UniFi Switch US-24 250W
* Ubiquiti UniFi AP-AC-Pro (Apartment, basement, underground parking)
* Ubiquiti UniFi controller on a datacenter VM (to manage all of the above)

### Phone

Another Fritz!Box 7412 just for VoIP connections.

Gigaset DECT base station connected to Fritz!Box and some DECT handsets.

### digitalSTROM

Light and shutter control system, see https://www.digitalstrom.com/

* dSS IP to manage the digitalSTROM installation and provide the API
* dSS 1GB as gateway to the digitalSTROM bus system, controlled by the dSS IP

### Zigbee

Running [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt) on a Raspberry Pi 3 Model B using a [CC2531](https://www.amazon.de/dp/B07JBWF1DG) zigbee sniffer with [source routing firmware](https://github.com/Koenkk/Z-Stack-firmware/tree/master/coordinator/Z-Stack_Home_1.2/bin/source_routing).
Using IKEA Trådfri bulbs and OSRAM smart+ plugs as routers.

## Ecosystem

### Wall switches

* [digitalSTROM](https://productinfo.digitalstrom.com/4290046000904/)

### Lights

* [digitalSTROM](https://productinfo.digitalstrom.com/4290046000010/)
* Trådfri light bulbs (zigbee)
* [DD001-MINI LED strip controllers](https://templates.blakadder.com/DD001-MINIG-IR-V08.html) (zigbee)

### Shutters

* [digitalSTROM](https://productinfo.digitalstrom.com/4290046000607/)

### Media

* Sonos
* Some Google Home
* Some Amazon Echo
* Some FireTV
* Synology DS212j
* Alexa media player
* LG WebOS TV

### Presence detection

* UniFi device tracker
* Home Assistant mobile app

### Sensors

* Met.no weather
* DarkSky weather
* Waze travel time
* Home Assistant mobile app on Android/iOS devices
* Xiaomi Aqara window/door sensors (zigbee)
* Xiaomi Aqara climate sensors (zigbee)
* Xiaomi Aqara water leakage sensors (zigbee)
* Xiaomi Aqara occupancy sensors (zigbee)
* Xiaomi MiFlora plant sensors (via [ESP32 BLE gateway running ESPHome](https://esphome.io/components/sensor/xiaomi_miflora.html))

### Power plugs

* TP Link HS110
* OSRAM smart+ plugs (zigbee)
* Lots of ESP8266 based tasmota plugs
  [Gosund SP111 single switches](https://templates.blakadder.com/gosund_SP111.html)
  [Klas Remo single switches](https://templates.blakadder.com/SWA11.html)
  [AOFO 4AC + 4USB](https://templates.blakadder.com/aofo_4AC4USB.html)
  

### Utility

* Xiaomi Roborock vacuum gen2 running Valetudo

### Spare ecosystem

* Xiaomi Aqara magic cube (zigbee)
