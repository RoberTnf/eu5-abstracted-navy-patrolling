#!/usr/bin/env python3
"""Build the Abstracted Navy Patrolling GUI file from vanilla:
    mod/in_game/gui/seazone_window.gui

Run after every EU5 update:
    python3 scripts/anp-build-gui.py

Copies vanilla in_game/gui/seazone_window.gui and inlines a checkbox next to the header's pin
button that adds/removes the sea zone from the player's patrolled zones (scripted GUIs
anp_toggle_zone / anp_zone_patrolled). Inlined, not via a template: widgets added through
`using = <template>` never showed up in game.

Fails loudly if vanilla changed in a way the patch no longer fits.
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.environ.get('EU5_GAME_DIR') or os.path.expanduser(
    '~/.local/share/Steam/steamapps/common/Europa Universalis V/game')
VANILLA_GUI = os.path.join(GAME, 'in_game/gui/seazone_window.gui')
OUT = os.path.join(REPO, 'mod/in_game/gui/seazone_window.gui')

ANCHOR = '''						tooltipwidget = { BasicFunctionalTooltip = {} }
						down = "[IsSeazoneFaved(Location.Self)]"
					}
'''

SCOPE = "GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('anp_zone', Location.MakeScope).End"

BUTTON = f'''
					button_checkbox = {{
						name = "anp_patrol_zone"
						size = {{ 23 23 }}
						visible = "[IsPlayerValid]"
						datacontext = "[SeaZoneView.GetLocation]"
						down = "[GetScriptedGui('anp_zone_patrolled').IsShown({SCOPE})]"
						onclick = "[GetScriptedGui('anp_toggle_zone').Execute({SCOPE})]"
						tooltip = "ANP_PATROL_ZONE_TT"
					}}
'''


def main():
    s = open(VANILLA_GUI, 'rb').read().decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    n = s.count(ANCHOR)
    if n != 1:
        sys.exit(f'ERROR: expected exactly one pin button in vanilla seazone_window.gui, found {n}. '
                 'Vanilla changed; update scripts/anp-build-gui.py.')
    s = s.replace(ANCHOR, ANCHOR + BUTTON)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(s.replace('\n', newline))
    print(f'Wrote {OUT}')


if __name__ == '__main__':
    main()
