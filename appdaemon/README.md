# Concept

Automations are split in two parts: Setting a status and changing device behavior based on a status.

# Utilities

## Delayer

Most lights and all covers in my installation are controlled by digitalSTROM. This system can easily be overwhelmed if too many statuses are changed at the same time. Since AppDaemon is async all device updates will be triggered at almost the same time.
Delayer is a simple FIFO stack that executes one queued item each second.
See [UtilDelayer](./apps/UtilDelayer)

## Announcer

Central service to play announcements on a media player.
See [UtilAnnouncer](./apps/UtilAnnouncer)

# Statuses

* Presence (by digitalSTROM)
* Sleeping (by digitalSTROM)
* Darkness (based on sunset/sunrise)
  see [StateDarkness](./apps/StateDarkness)
* Sun protection (manually activated, based on time of day)
  see [StateSunprotection](./apps/StateSunprotection)
* Window open/closed (based on Xiaomi window sensor)
* Nightly watering cycle
  see [StateWateringNight](./apps/StateWateringNight)
* Vacuum cleaning status
  see [StateVacuum](./apps/StateVacuum)
* Laundry status based on machine power consumption
  see [StateLaundry](./apps/StateLaundry)

# Automations

## Presence, leaving, returning

Announce status change
See [ActionPresence](./apps/ActionPresence)

## Cover control

Update cover status based on presence/absence, sleeping/awake, night/day, sun protection on/off, window open/closed and presence detection.
See [ActionCover](./apps/ActionCover)

## Light control

Update light status based on presence/absence, sleeping/awake, night/day.
See [ActionLight](./apps/ActionLight)

## Fan control
* Turn on the bathroom/shower fan when the main room light is turned on.
  Keep it running for some more minutes when the light has been turned off.
* Start fan on/off cycle when absent to get more fresh air in the apartment.
See [ActionFan](./apps/ActionFan)

## Generic state change responder
Set the status of a device according to the status of another device.
Used to turn on zigbee lights when a digitalSTROM light (scene) is turned on.
See [ActionResponder](./apps/ActionResponder)

## Watering

Lawn watering cycles.
See [ActionWatering](./apps/ActionWatering)

## Vacuum cleaning

Vacuum as long as noone is home, pause cycle when someone returns and continue later on.
See [ActionVacuum](./apps/ActionVacuum)

# Notifications

## Laundry

Announce when the laundry is done.
See [NotifyLaundry](./apps/NotifyLaundry)
