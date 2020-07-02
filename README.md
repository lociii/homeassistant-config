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
* Nicholas Alipaz (Dynamic DNS updater)
  https://github.com/nalipaz/hassio-addons
* Markus Pöschl (i.a. Valetudo mapper)
  https://github.com/Poeschl/Hassio-Addons
* Home Assistant Community Edge Addons (Network UPS Tools)
  https://addons.community/edge

## Automations

100% of my automations are using the [automations editor](automations.yaml) and the frontend defined helpers.

## Custom components - HACS

The [Home Assistant Community Store](https://hacs.xyz/), a project started by [@ludeeus](https://twitter.com/ludeeus) to make installing and managing non-core components much easier. Thank you so much for your great work!

HACS is used to install and manage my custom components, lovelace plugins and lovelace themes.
The following components are essential to my setup:

### digitalSTROM

My [homegrown component](https://github.com/lociii/homeassistant-digitalstrom) to control my lights and shutters which are based on [digitalSTROM](https://www.digitalstrom.com/).

Check out the underlying library for more details: [pydigitalstrom](https://github.com/lociii/pydigitalstrom)

### CS:GO game state

My [homegrown component](https://github.com/lociii/homeassistant-csgo) to automate my home according to the state of the CS:GO game I'm playing.

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

Running [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt) on a Raspberry Pi 4 (4GB) using a [Texas Instruments LAUNCHXL-CC26X2R1](http://www.ti.com/tool/LAUNCHXL-CC26X2R1) zigbee sniffer with ZStack 3.0 firmware](https://github.com/Koenkk/Z-Stack-firmware/blob/master/coordinator/Z-Stack_3.x.0/bin/CC26X2R1_20200417.zip).
Using IKEA Trådfri bulbs, some Hue bulbs/strips and OSRAM smart+ plugs as routers.

## Ecosystem

### Wall switches

* [digitalSTROM](https://productinfo.digitalstrom.com/4290046000904/)

### Lights

* [digitalSTROM](https://productinfo.digitalstrom.com/4290046000010/)
* Trådfri light bulbs (zigbee)
* Philips Hue light strip plus (zigbee)
* Philips Hue bulbs (zigbee) 

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

### Other actors

* Xiaomi MiJia wireless switch (zigbee)

### Sensors

* Met.no weather
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
* Lots of ESP8266 based plugs running on [ESPHome](esphome/)
  + [Gosund SP111 single switches](https://templates.blakadder.com/gosund_SP111.html)
  + [Klas Remo single switches](https://templates.blakadder.com/SWA11.html)
  + [AOFO 4AC + 4USB](https://templates.blakadder.com/aofo_4AC4USB.html)

### UPS

* Eaton Ellipse Pro 650 UPS
  Monitored via Network UPS Tools (Home Assistant Supervisor addon)

### Utility

* Xiaomi Roborock S50 vacuum running Valetudo

### Spare ecosystem

* Xiaomi Aqara magic cube (zigbee)
