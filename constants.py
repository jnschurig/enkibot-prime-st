
ENKI_DATA_URL = 'https://enkibot-prime.herokuapp.com/debug/'

CLASS_CODE_LOOKUP = {
    'Knight': {'code': 'KGT', 'crystal': 'WIND'},
    'Monk': {'code': 'MNK', 'crystal': 'WIND'},
    'Thief': {'code': 'THF', 'crystal': 'WIND'},
    'Black-Mage': {'code': 'BLM', 'crystal': 'WIND'},
    'White-Mage': {'code': 'WHM', 'crystal': 'WIND'},
    'Blue-Mage': {'code': 'BLU', 'crystal': 'WIND'},
    'Mystic-Knight': {'code': 'MYS', 'crystal': 'WATER'},
    'Time-Mage': {'code': 'TIM', 'crystal': 'WATER'},
    'Summoner': {'code': 'SUM', 'crystal': 'WATER'},
    'Red-Mage': {'code': 'RDM', 'crystal': 'WATER'},
    'Berserker': {'code': 'BER', 'crystal': 'WATER'},
    'Beastmaster': {'code': 'BST', 'crystal': 'FIRE'},
    'Geomancer': {'code': 'GEO', 'crystal': 'FIRE'},
    'Ninja': {'code': 'NIN', 'crystal': 'FIRE'},
    'Bard': {'code': 'BRD', 'crystal': 'FIRE'},
    'Ranger': {'code': 'RAN', 'crystal': 'FIRE'},
    'Samurai': {'code': 'SAM', 'crystal': 'EARTH'},
    'Dragoon': {'code': 'DRG', 'crystal': 'EARTH'},
    'Dancer': {'code': 'DNC', 'crystal': 'EARTH'},
    'Chemist': {'code': 'CHM', 'crystal': 'EARTH'},
    'Freelancer': {'code': 'FRE', 'crystal': 'INNATE'},
    'Mime': {'code': 'MIM', 'crystal': 'WATER'},
    'Cannoneer': {'code': 'CAN', 'crystal': 'ADVANCE'},
    'Gladiator': {'code': 'GLD', 'crystal': 'ADVANCE'},
    'Oracle': {'code': 'ORC', 'crystal': 'ADVANCE'},
}

UNKNOWN_OPTIONS = [
    'UNKNOWN WIND',
    'UNKNOWN WATER',
    'UNKNOWN FIRE',
    'UNKNOWN EARTH',
]

HINT_DB_FILE_NAME = 'hint_db.md'

PAGE_ICONS = [
    '⚔️',
    '🗡️',
    '🛡️',
    '🔪',
    '🏹',
    '🎀',
    '🪄',
    '🔔',
    # '🤜🏽',
    '🎶',
    # '📖',
    '⛺',
    # '🧪',
    '⚗️',
    # '📜',
    '🔨',
]

ABOUT_TEXT = '''
A [Four Job Fiesta](https://www.fourjobfiesta.com/) hint generator.

This is a shameless ripoff of the original [Enkibot Prime](https://enkibot-prime.herokuapp.com/).
This version was made using Python and Streamlit and has enriched content and functionality. 
Check out the [Github Repo](https://github.com/jnschurig/enkibot-prime-st). All hint data was ripped 
from the original app and all credit goes to the original creators.
'''

SECTION_NAV_ANCHORS = {
    'Post-Wind Shrine': 'World 1',
    'World 2 Intro': 'World 2',
    'Antlion': 'World 3',
}
