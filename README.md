[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

# My HomeAssistant setup

Hi, I'm Jens and this is how I set up my home automation using HomeAssistant.  
One of the main targets is to use devices which don't rely on cloud services wherever possible.

## HomeAssistant environment

### NUC

NUC7I5BNK with Core i5 7260U, 16GB RAM and 500GB Samsung 970 EVO Plus M2 SSD.  
This machine is called "ship".

### Home Assistant environment

Home Assistant itself is run supervised on Debian 10, check the instructions [here](https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md).

Official addons in use:
* Config check  
* Let's encrypt  
* MariaDB  
* Mosquitto  
* NGINX SSL proxy

Custom supervisor addons in use:
* ESPHome https://github.com/esphome/hassio
  * ESPHome dashboard
* Home Assistant Community Addons https://github.com/hassio-addons/repository  
  * Bitwarden (Vaultwarden)
  * FTP
  * Glances
  * Network UPS Tools
  * Portainer
  * Node Red
  * Visual Studio Code
  * WireGuard VPN
* Moshe https://github.com/TheBestMoshe/home-assistant-addons  
  * Paperless NG
* eightiesguy https://github.com/haberda/hassio_addons  
  * Signal messenger
* Stephen Beechen https://github.com/sabeechen/hassio-google-drive-backup  
  * Google Drive backup
* Markus Pöschl https://github.com/Poeschl/Hassio-Addons  
  * Valetudo mapper

## Automations

Most of my automations are defined in [Node RED](https://nodered.org/) using [Frenck's](https://github.com/frenck) awesome [addon](https://github.com/hassio-addons/addon-node-red).

Some are still defined with the [automations editor](automations.yaml) but I'm on my way of migrating them too.

## Custom components - HACS

The [Home Assistant Community Store](https://hacs.xyz/), a project started by [@ludeeus](https://twitter.com/ludeeus) to make installing and managing non-core components much easier. Thank you so much for your great work!

HACS is used to install and manage my custom components, lovelace plugins and lovelace themes.
The following components are essential to my setup:

### Alexa Media Player

https://github.com/custom-components/alexa_media_player

This is a custom component to allow control of Amazon Alexa devices in Home Assistant using the unofficial Alexa API.

### Average sensor

https://github.com/Limych/ha-average

Calculate averages of values over time

## Infrastructure

### Internet connection

Main 1000M/50M cable -> Fritz!Box 6591 Cable -> UniFi USG Pro

Backup 100M50M DSL -> Fritz!Box 7412 (PPPoE passthrough only) -> UniFi USG Pro

### Network

* Ubiquiti UniFi USG Pro
* Ubiquiti UniFi Switch US-24 250W
* Ubiquiti UniFi AP-AC-Pro (2x apartment, basement, underground parking)
* Ubiquiti UniFi controller on a datacenter VM (to manage all of the above)

### Phone

Another Fritz!Box 7412 just for VoIP connections.

Gigaset DECT base station connected to Fritz!Box and some DECT handsets.

### Zigbee

Direct integration with ZHA in HomeAssistant. I'm forwarding the USB device of the controller by network as the NUC is placed in the basement and the zigbee controller should be located in the apartment. See #17

Controller is a [Texas Instruments LAUNCHXL-CC26X2R1](http://www.ti.com/tool/LAUNCHXL-CC26X2R1) zigbee sniffer with [ZStack 3.0 firmware](https://github.com/Koenkk/Z-Stack-firmware/blob/master/coordinator/Z-Stack_3.x.0/bin/CC26X2R1_20200417.zip) connected to as Raspberry Pi 3.

## Ecosystem

I'm heavily relying on ESP based actors and sensors. Please see my [ESPHome README](esphome/) for more details.

### Wall switches

* [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) running [ESPHome](esphome/common/device_shelly25.yaml)

### Lights

* [Shelly 1](https://shelly.cloud/products/shelly-1-smart-home-automation-relay/) running [ESPHome](esphome/common/device_shelly1.yaml)
* [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) running [ESPHome](esphome/common/device_shelly25.yaml)
* [MagicHome RGB LED controller](https://tasmota.github.io/docs/devices/MagicHome-LED-strip-controller/) running [ESPHome](esphome/common/device_magichome.yaml)
* Trådfri light bulbs (zigbee)
* Ledvance Smart+ light bulbs (zigbee)
* Philips Hue light strip plus (zigbee)

### Shutters

* [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) running [ESPHome](esphome/common/template_cover_timebased.yaml)

### Media

* Sonos
* Some Google Home
* Some Amazon Echo
* Some FireTV
* Synology DS212j
* LG WebOS TV

### Presence detection

* UniFi device tracker
* Home Assistant mobile app

### Other devices

* Xiaomi MiJia wireless switch (zigbee)
* Met.no weather
* Waze travel time
* Home Assistant mobile app on Android/iOS devices
* Xiaomi Aqara window/door sensors (zigbee)
* Xiaomi Aqara climate sensors (zigbee)
* Xiaomi Aqara water leakage sensors (zigbee)
* Xiaomi Aqara occupancy sensors (zigbee)
* Bitron AV2010/32 wall thermostat to control the underfloor heating

### Power plugs

* Lots of ESP8266 based plugs running on ESPHome - see my [ESPHome config for details](esphome/)
  + [Gosund SP111 single plugs](https://templates.blakadder.com/gosund_SP111.html) running [ESPHome](esphome/common/device_sp111.yaml)
  + [Gosund SP112 single plugs with USB](https://templates.blakadder.com/gosund_SP112.html) running [ESPHome](esphome/common/device_sp112_v28.yaml)
  + [AOFO 4AC + 4USB](https://templates.blakadder.com/aofo_4AC4USB.html) running [ESPHome](esphome/common/device_aofo_4ac4usb.yaml)

### UPS

* Eaton Ellipse Pro 650 UPS  
  Monitored via Network UPS Tools (Home Assistant Supervisor addon)

### Utility

* Xiaomi Roborock S50 vacuum running [Valetudo](https://github.com/Hypfer/Valetudo)
