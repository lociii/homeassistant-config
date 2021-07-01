# ESPHome

All ESP8266 based components in my home are running on [ESPHome](https://esphome.io/).

Most of the configs are based on forum threads and the [Tasmota](https://tasmota.github.io) [templates](https://tasmota.github.io/docs/Components/) for them.

## Config structure

The configuration is package based and as modular and reusable as possible.
Packages are structured by
* Shared defaults (API, OTA, version sensors, etc.)
* WiFi settings (Main floor WiFi, basement WiFi)
* Board (ESP01, ESP8285, etc.)
* Device (Shelly1, Shelly2.5, SP111, etc.)
* Usage template (Fan, switch, light, etc.)

Devices always only define outputs. The usage templates then convert these outputs to components that are exposed in Home Assistant.

e.g. The [GoSund SP112](common/device_sp112_v28.yaml) defines one output for AC (a) and one output for USB (b).
A physical device now just needs to add the WiFi and device packages and define how the output should be exposed as a component, see the [bedroom charging plug](sp112_plug_bedroom_charging.yaml) for an example.

## Devices

### Power plugs

#### Gosund SP111

Single plug with power measurement

* [Tasmota template v1.0](https://templates.blakadder.com/gosund_SP111.html)
* [Tasmota template v1.1](https://templates.blakadder.com/gosund_SP111_v2.html)
* [Tasmota template v1.4](https://templates.blakadder.com/gosund_SP111_v1_4.html)

[Device type template](common/device_sp111.yaml)

Device differences

| Pin       | v1.0         | v1.1        | v1.4        |
| --------- | ------------ | ----------- | ----------- |
| GPIO00    |  Led1i       | Led1i       | Led2i       |
| GPIO01    |  None        | None        | User        |
| GPIO02    |  Led2i       | LedLinki    | Led1i       |
| GPIO03    |  None        | None        | User        |
| GPIO04    |  None        | HLWBL CF1   | None        |
| GPIO05    |  BL0937 CF   | BL0937 CF   | BL0937 CF   |
| GPIO09    |  None        | None        | None        |
| GPIO10    |  None        | None        | None        |
| GPIO12    |  HLWBL SELi  | HLWBL SELi  | HLWBL SELi  |
| GPIO13    |  Button1     | Button1     | Button1     |
| GPIO14    |  HLWBL CF1   | None        | HLWBL CF1   |
| GPIO15    |  Relay1      | Relay1      | Relay1      |
| GPIO16    |  None        | None        | None        |
| FLAG      |  None        | None        | None        |

#### Gosund SP112

Single plug with power measurement and switchable USB ports.

**There are two different versions on the market which are almost indistinguishable from the outside!!!**
The print on the backside of the devices is slightly bolder and larger on v3.4 compared to v2.8.

SP112 v3.4 is almost similar from it's inner parts to the SP111 v1.4

* [Tasmota template v2.8](https://templates.blakadder.com/gosund_SP112.html)
* [Tasmota template v3.4](https://templates.blakadder.com/gosund_SP112_v3_4.html)

[Device type template v2.8](common/device_sp112_v28.yaml)
[Device type template v3.4](common/device_sp112_v34.yaml)

Device differences

| Pin       | v2.8          | v3.4          |
| --------- | ------------- | ------------- |
| GPIO00    |  Led2i        | Led1i         |
| GPIO01    |  CSE7766 Tx   | None          |
| GPIO02    |  Led1i        | Led2i         |
| GPIO03    |  CSE7766 Rx   | None          |
| GPIO04    |  User         | HLWBL CF1     |
| GPIO05    |  Relay2       | BL0937 CF     |
| GPIO09    |  None         | None          |
| GPIO10    |  None         | None          |
| GPIO12    |  User         | HLWBL SELi    |
| GPIO13    |  User         | Relay2i       |
| GPIO14    |  Relay1       | Relay1        |
| GPIO15    |  User         | None          |
| GPIO16    |  Button1      | None          |
| FLAG      |  None         | Buttoni       |

#### AOFO strip

Power strip with four mains outlets and four USB ports

* [Tasmota template](https://templates.blakadder.com/aofo_4AC4USB.html)

[Device type template](common/device_aofo_4ac4usb.yaml)

### LED controllers

#### Magic Home

Controls RGB light strips

* [Tasmota template](https://templates.blakadder.com/magichome_ZJ-FWMN-A_RGB.html)

[Device type template](common/device_magichome.yaml)

### Shelly switches / actors

All my inputs are momentary switches! You may need to adjust some templates if you're using regular on/off switches.

#### Shelly 1

One input, one output

* [Tasmota template](https://templates.blakadder.com/shelly_1.html)
* [Shelly knowledge base](https://shelly.cloud/support/knowledge-base/shelly-1/#wiring)
* Wiring diagrams [1](https://www.shelly-support.eu/lexikon/index.php?entry/47-connection-diagrams-shelly-1/) / [2](https://www.shelly-support.eu/lexikon/index.php?entry/58-anschlussschemen-shelly-1-fortsetzung/)

[Device type template](common/device_shelly1.yaml)

#### Shelly 2.5

Two inputs, two outputs, power measurement.

Used for switch inputs (sensors), lights, fans and covers.

* [Tasmota template](https://templates.blakadder.com/shelly_25.html)
* [Shelly knowledge base](https://shelly.cloud/support/knowledge-base/shelly-25/#wiring)
* Wiring diagrams [1](https://www.shelly-support.eu/lexikon/index.php?entry/48-connection-diagrams-shelly-2-5/) / [2](https://www.shelly-support.eu/lexikon/index.php?entry/100-connection-diagrams-shelly-2-5-continuation/)
* [Power monitor hints](https://esphome.io/components/sensor/ade7953.html)

[Device type template](common/device_shelly25.yaml)

#### Shelly RGBW2

Control LED light strips.

* [Tasmota template](https://templates.blakadder.com/shelly_RGBW2.html)
* [Shelly knowledge base](https://shelly.cloud/knowledge-base/devices/shelly-rgbw2/#wiring)
* Wiring diagrams [1](https://www.shelly-support.eu/lexikon/index.php?entry/53-connection-diagrams-shelly-rgbw2/) / [2](https://www.shelly-support.eu/lexikon/index.php?entry/180-connection-diagrams-shelly-rgbw2-continuation/)

[Device type template](common/device_shellyrgbw2.yaml)

Example devices:
* Warm/cold white control on a WOFI ceiling fixture ([9693.01.70.5200](https://www.amazon.de/gp/product/B00LUKGN0K/)), see [kitchen ceiling light](shellyrgbw_light_kitchen_ceiling.yaml).

## Templates

### Time based covers

As my covers don't have a proper end stop reporting, I opted to use a [time based cover](common/template_cover_timebased.yaml) setup.

## ESPTool

Just listed here because I'm bad at remembering such commands.

### Read original flash

`esptool.py --p /dev/ttyUSB0 read_flash 0x00000 0x200000 <filename.bin>`

### Flash new firmware

`esptool.py --p /dev/ttyUSB0 write_flash -fs 1MB -fm dout 0x0 <filename.bin>`
