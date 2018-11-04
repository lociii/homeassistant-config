# Concept

Automations are split in two parts: Setting a status and changing device behavior based on a status.

# Utilities

## Delayer

Most lights and all covers in my installation are controlled by digitalSTROM. This system can easily be overwhelmed if too many statuses are changed at the same time. Since AppDaemon is async all device updates will be triggered at almost the same time.  
Delayer is a simple FIFO stack that executes one queued item each second.  
See [utilDelayer](./utilDelayer)

## Announce

Central service to play announcements on a media player.  
See [announce](./announce)

# Statuses

* Presence (by digitalSTROM)
* Sleeping (by digitalSTROM)
* Darkness (based on sunset/sunrise)  
  see [stateDarkness](./stateDarkness)
* Sun protection (manually activated, based on time of day)
* Window open/closed (based on Xiaomi window sensor)

# Automations

## Leaving home

Flash defined lights, announce absence and start fan cycle.  
See [actionLeavingHome](./actionLeavingHome)

## Coming home

Announce presence, turn on some lights when it's dark.  
See [actionComingHome](./actionComingHome)

## Cover control

Update cover status based on presence/absence, sleeping/awake, night/day, sun protection on/off and if the window is open or closed.  
See [actionCover](./actionCover)

## Light control

Update light status based on presence/absence, sleeping/awake, night/day.  
See [actionLight](./actionLight)

## Watering

Lawn watering cycles.  
See [watering](./watering)

# Responders

## Bathroom/shower fan

Turn on the bathroom/shower fan when the main room light is turned on. Keep it running for some more minutes when the light has been turned off.  
See [actionFan](./actionFan)

## Reading light

The reading light can be controlled by a digitalSTROM wall switch. Turn on/off the light when the switch is toggled.  
See [readinglight](./readinglight)

# Notifications

## Laundry

Announce when the laundry is done based on the power usage of the washing machines/dryer.  
See [laundry](./laundry)