
# ESPHome

All ESP8266 based components in my home are running on [ESPHome](https://esphome.io/) by [Otto Winter](https://github.com/OttoWinter) and a [big bunch of contributors](https://github.com/esphome/esphome/graphs/contributors).

Most of the configs are based on forum threads and the [Tasmota](https://tasmota.github.io) [templates](https://tasmota.github.io/docs/Components/) for them.

## Config structure

My device configs are split into several files to make them reusable.

* [Defaults](.defaults.yaml) - used in every device type template
* [Device type templates](#devices) that define specific behavior of a certain device like the [SP111 plug](#gosund-sp111)
* Device configs that specify a single, physical device with their name (substitutes) and device specific settings like actors

## ESPTool

Just listed here because I'm bad at remembering such commands.

### Read original flash

`esptool.py --p /dev/ttyUSB0 read_flash 0x00000 0x200000 <filename.bin>`

### Flash new firmware

`esptool.py --p /dev/ttyUSB0 write_flash -fs 1MB -fm dout 0x0 <filename.bin>`

## Devices

### Power plugs

#### Gosund SP111

Single plug with power measurement

* [Tasmota template v1.0](https://templates.blakadder.com/gosund_SP111.html)
* [Tasmota template v1.1](https://templates.blakadder.com/gosund_SP111_v2.html)
* [Tasmota template v1.4](https://templates.blakadder.com/gosund_SP111_v1_4.html)

[Device type template](.sp111.yaml)

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

Single plug with power measurement and two switchable USB ports.

**There are two different versions on the market which are almost indistinguishable from the outside!!!**
The print on the backside of the devices is slightly bolder and larger on v3.4 compared to v2.8.

SP112 v3.4 is almost similar from it's inner parts to the SP111 v1.4

* [Tasmota template v2.8](https://templates.blakadder.com/gosund_SP112.html)
* [Tasmota template v3.4](https://templates.blakadder.com/gosund_SP112_v3_4.html)

[Device type template](.sp112_v28.yaml)
[Device type template](.sp112_v34.yaml)

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

#### Klas Remo SWA11

Single plug with power measurement

* [Tasmota template](https://templates.blakadder.com/SWA11.html)

[Device type template](.swa11.yaml)

#### AOFO strip

Power strip with four outlets and four USB ports

* [Tasmota template](https://templates.blakadder.com/aofo_4AC4USB.html)

[Device type template](.aofo_4ac4usb.yaml)

### LED controllers

#### Magic Home

Controls RGB light strips

* [Tasmota template](https://templates.blakadder.com/magichome_ZJ-FWMN-A_RGB.html)

[Device type template](.magichome.yaml)

### Shelly switches

#### Shelly 1

One input, one output

* [Tasmota template](https://templates.blakadder.com/shelly_1.html)
* [Shelly knowledge base](https://shelly.cloud/support/knowledge-base/shelly-1/#wiring)
* Wiring diagrams [1](https://www.shelly-support.eu/lexikon/index.php?entry/47-connection-diagrams-shelly-1/) / [2](https://www.shelly-support.eu/lexikon/index.php?entry/58-anschlussschemen-shelly-1-fortsetzung/)

[Device type template](.shelly1.yaml) and [example device](.shelly1_example.yaml).

<!--
#### Shelly 1 PM

One input, one output, power measurement

* [Tasmota template](https://templates.blakadder.com/shelly_1PM.html)
* [Shelly knowledge base](https://shelly.cloud/support/knowledge-base/shelly-1/#wiring)
* [Wiring diagrams](https://www.shelly-support.eu/lexikon/index.php?entry/51-connection-diagrams-shelly-1pm/)
* [Instructions](https://github.com/arendst/Tasmota/issues/5716#issuecomment-589879170) to resolder some connections to measure voltage and amperage

[Device type template](.shelly1pm.yaml) - device needs to define the actual actor
-->

#### Shelly 2.5

Two inputs, two outputs, power measurement

* [Tasmota template](https://templates.blakadder.com/shelly_25.html)
* [Shelly knowledge base](https://shelly.cloud/support/knowledge-base/shelly-25/#wiring)
* Wiring diagrams [1](https://www.shelly-support.eu/lexikon/index.php?entry/48-connection-diagrams-shelly-2-5/) / [2](https://www.shelly-support.eu/lexikon/index.php?entry/100-connection-diagrams-shelly-2-5-continuation/)
* [Power monitor hints](https://esphome.io/components/sensor/ade7953.html)

[Device type template](.shelly25.yaml) and [example device](.shelly25_example.yaml).

<!--
#### Shelly i3

* [Shelly knowledge base: wiring](https://shelly.cloud/support/knowledge-base/shelly-i3/#wiring)
* [Shelly knowledge base: device pinout](https://shelly.cloud/support/knowledge-base/shelly-i3/#pinout)
* [Wiring diagrams](https://www.shelly-support.eu/lexikon/index.php?entry/212-connection-diagrams-shelly-i3/)

[Device type template](.shellyi3.yaml)

TODO
-->

### Mi Flora

Plant monitoring system based on BLE.
I'm running a single ESP32 board to read their broadcasts.

More info on the [ESPHome component](https://esphome.io/components/sensor/xiaomi_miflora.html).
