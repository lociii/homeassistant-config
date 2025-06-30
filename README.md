[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

# My HomeAssistant setup

Hi, I'm Jens and this is how I set up my home automation using HomeAssistant.  
One of the main targets is to use devices which don't rely on cloud services wherever possible.

## HomeAssistant environment

### NUC

NUC7I5BNK with Core i5 7260U, 16GB RAM and 500GB Samsung 970 EVO Plus M2 SSD running Home Assistant OS.  
This machine is called "ship".

### Home Assistant environment

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

Automations are mostly build in the Home Assistant [automation editor](automations.yaml). Some are still in [Node RED](https://nodered.org/) but they're getting migrated too.

I'm trying to build most repetitive automations in blueprints - sometimes it's a hustle as e.g. shutter automations vary by little but important details.

## Custom components - HACS

The [Home Assistant Community Store](https://hacs.xyz/), a project started by [@ludeeus](https://twitter.com/ludeeus) to make installing and managing non-core components much easier. Thank you so much for your great work!

HACS is used to install and manage my custom components, lovelace plugins and lovelace themes.
The following components are essential to my setup:

### Average sensor

https://github.com/Limych/ha-average

Calculate averages of values over time

## Infrastructure

### Internet connection

Main 1000M/50M cable -> Fritz!Box 6591 Cable -> UniFi USG Pro

Backup 100M/50M DSL -> Fritz!Box 7412 (PPPoE passthrough only) -> UniFi USG Pro

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

## ESPHome

I'm heavily relying on ESP based actors and sensors. Please see my [ESPHome README](esphome/) for more details.

#### Wall switches

* [Shelly Plus i4](https://www.shelly.com/en/products/shop/shelly-plus-i4)

#### Lights

* [Shelly 1 Mini](https://www.shelly.com/en/products/shop/shelly-1-mini-gen-3)
* [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/)
* [MagicHome RGB LED controller](https://tasmota.github.io/docs/devices/MagicHome-LED-strip-controller/)
* Trådfri light bulbs (zigbee)
* Ledvance Smart+ light bulbs (zigbee)
* Philips Hue light strip plus (zigbee)

#### Shutters

* [Shelly Plus 2PM](https://www.shelly.cloud/en/products/shop/shelly-plus-2-pm)

#### Power plugs

* [Shelly Plug Plus S](https://www.shelly.com/en/products/shop/shelly-plus-plug-s)
* Lots of ESP8266 based plugs running on ESPHome
  + [Gosund SP111 single plugs](https://templates.blakadder.com/gosund_SP111.html)
  + [Gosund SP112 single plugs with USB](https://templates.blakadder.com/gosund_SP112.html)
  + [AOFO 4AC + 4USB](https://templates.blakadder.com/aofo_4AC4USB.html)

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
* Home Assistant mobile app on Android/iOS devices
* Xiaomi Aqara window/door sensors (zigbee)
* Xiaomi Aqara climate sensors (zigbee)
* Xiaomi Aqara water leakage sensors (zigbee)
* Xiaomi Aqara occupancy sensors (zigbee)
* Bitron AV2010/32 wall thermostat to control the underfloor heating

### UPS

* Eaton Ellipse Pro 650 UPS  
  Monitored via Network UPS Tools (Home Assistant Supervisor addon)

### Utility

* Xiaomi Roborock S50 vacuum running [Valetudo](https://github.com/Hypfer/Valetudo)
