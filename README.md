# Abstracted Navy Patrolling

A Europa Universalis V mod (game version 1.4.*). Adds the naval ability **Abstracted Patrol**: patrolling fleets pool their maritime presence and spread it every month over the sea zones you pick, without the Patrol the Seas AI moving your ships around. Player-facing description: [`workshop.txt`](workshop.txt) (Steam BBCode).

## Layout

| Path | What |
|------|------|
| `mod/` | The mod itself; this folder is what goes into the EU5 `mod/` directory and gets uploaded to the Workshop |
| `scripts/anp-build-gui.py` | Generates `mod/in_game/gui/seazone_window.gui` (vanilla + the patrol checkbox) |
| `scripts/anp-build-values.py` | Generates `mod/in_game/common/script_values/anp_ship_values.txt` (per-ship maritime presence lookup) |
| `workshop.txt` | Steam Workshop description |

## After every EU5 update

```bash
python3 scripts/anp-build-gui.py
python3 scripts/anp-build-values.py
```

Both outputs are generated; never edit them by hand. The scripts read the game from `~/.local/share/Steam/steamapps/common/Europa Universalis V/game`; set `EU5_GAME_DIR` to point them elsewhere.

## How it works

- Toggle naval ability `anp_patrol`. Monthly (`monthly_country_pulse` → `anp_monthly_pulse`, human players only, `change_maritime_presence_power`): every fleet with it on that is at sea and out of combat (`anp_is_projecting`) **pools** its presence. A fleet's presence (`anp_fleet_presence`) is the sum of its ships' vanilla `maritime_presence` × (1 + the country's `global_maritime_presence_modifier`) × `anp_presence_scale`. The pool is split evenly over every **patrolled zone**. With no patrolled zones, each fleet covers the non-lake sea zones of its own sea area instead.
- Patrolled zones are the country variable list `anp_zones`, toggled by a checkbox next to the pin button in the sea zone window (scripted GUIs `anp_toggle_zone` / `anp_zone_patrolled`), filled by decision `anp_patrol_coastal_waters` and cleared by `anp_stop_all_patrols`. Lakes are excluded (`anp_is_patrollable_zone`).
- `anp_presence_scale` = 1 is the vanilla rate; tune it in `mod/in_game/common/script_values/anp_values.txt`.
- Script can't read a ship's maritime presence, so `anp_ship_maritime_presence` is a generated `sub_unit_type` lookup. A unit type with `copy_from` **adds** its own `maritime_presence` to the inherited one (confirmed in game: a jong is light ship 0.2 + its own 0.08), so the generator sums along the chain. Ship types from other mods get `ship_small_maritime`.
- `change_maritime_presence_power` adds directly, so it never shows in a zone's monthly breakdown, and a `local_maritime_presence` modifier on a sea zone credits nobody. Patrolled zones get a display-only `anp_patrolled_waters` modifier sized to this month's per-zone amount, which is also stored in country variable `anp_zone_presence` for the checkbox tooltip.
- The ability adds static unit modifier `anp_patrolling` on start and removes it on finish, because script can only detect abilities through `has_unit_modifier`. A fleet split off a patrolling one starts with the ability off; merging keeps it on if either fleet had it.
- `seazone_window.gui` is a whole-file replacement (the checkbox sits in the top-level `lateralview`, not in a template).
- Localization ships for all 11 languages (English text for now; translations welcome).
