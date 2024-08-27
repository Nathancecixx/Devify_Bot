"""
+------------------------------------------------------------+
| * Devify is a discord bot written in python which adds   * |
| * easy developer communication templates to discord      * |
|                                                            |
|                                                            |
| * Devify                                                 * |
| * fall 24 - Nathan Ceci                                  * |
+------------------------------------------------------------+
"""

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'
