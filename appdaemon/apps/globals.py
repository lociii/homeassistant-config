# define times
DAY_START = 'sunrise'
NIGHT_START = 'sunset + 00:15:00'
NIGHT_OFFSET_LIGHT = -900
NIGHT_OFFSET_COVER = 900

HALLWAY_LIGHT = 'light.flur__flur'

# all covers
COVERS_ALL = [
    'cover.schlafzimmer__rolladen_schlafzimmer',
    'cover.arbeitszimmer__rolladen_arbeitszimmer',
    'cover.gastezimmer__rolladen_gastezimmer',
    'cover.wohnzimmer__rolladen_kuche',
    'cover.wohnzimmer__rolladen_esstisch',
    'cover.wohnzimmer__rolladen_terrasse',
    'cover.wohnzimmer__rolladen_couch',
]
# all lights
LIGHTS_ALL = [
    'light.flur__flur',
    'light.schlafzimmer__bettlicht',
    'light.schlafzimmer__deckenlicht',
    'light.gastezimmer__deckenlicht',
    'light.arbeitszimmer__deckenlicht',
    'light.bad__deckenlicht',
    'light.bad__spiegellicht',
    'light.dusche__deckenlicht',
    'light.dusche__spiegellicht',
    'light.kuche__deckenlicht',
    'light.kuche__schranklicht',
    'light.kuche__spulenlicht',
    'light.kuche__thekenlicht',
    'light.wohnzimmer__deckenlampe',
    'light.wohnzimmer__stehlampe',
    'light.wohnzimmer__wandlampen',
    'light.wohnzimmer__esstisch',
    'light.garten__laterne',
    'light.garten',
]

# covers that should be closed at night when present
COVERS_NIGHT_PRESENT = [
    'cover.schlafzimmer__rolladen_schlafzimmer',
    'cover.arbeitszimmer__rolladen_arbeitszimmer',
    'cover.gastezimmer__rolladen_gastezimmer',
    'cover.wohnzimmer__rolladen_kuche',
    'cover.wohnzimmer__rolladen_esstisch',
    'cover.wohnzimmer__rolladen_couch',
]
# covers that should be closed at night when absent
COVERS_NIGHT_ABSENT = COVERS_NIGHT_PRESENT + [
    'cover.wohnzimmer__rolladen_terrasse',
]

# lights that should go on at night when absent
LIGHTS_NIGHT_ABSENT = [
    'light.wohnzimmer__wandlampen',
    'light.garten__laterne',
    'light.garten',
]
# lights that should go on at night when present
LIGHTS_NIGHT_PRESENT = [
    'light.wohnzimmer__stehlampe',
] + LIGHTS_NIGHT_ABSENT

# lights that should be on at night when returning home
LIGHTS_NIGHT_RETURNING = [
    'light.flur__flur',
    'light.kuche__schranklicht',
] + LIGHTS_NIGHT_PRESENT

FANS = [
    'light.bad__lufter',
    'light.dusche__lufter',
]

GOOGLE_TTS_DEVICE = 'media_player.wohnzimmer'

SENSOR_APARTMENT_PRESENCE = 'sensor.apartment__present'
SENSOR_APARTMENT_SLEEPING = 'sensor.apartment__sleeping'