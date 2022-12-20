# Custom Mektools edit for FFXIV Zones in Blender

Custom edit of MekTools that adds a couple functions that are recommended when importing FFXIV zones as fbx in Blender (for details see https://forums.nexusmods.com/index.php?showtopic=12190758/#entry117011953).
Did it mostly so I don't have to select and apply those modifications to each object individually every time I import a zone.

When used, the script will go through a scene's materials and change the following properties for each (no need to have anything selected):
- Normal Map Shader to World Space
- Normal Map Shader Strength to 50%

### To install and use:
- Download and install the original MekTools version from Meku's discord server (see below, currently version 0.33).
- Download \_\_init.py\_\_ from this repo and replace the \_\_init.py\_\_ in MekTools' installation folder in Blender addons' folder.
- There should now be a sub-menu ("Zone Adjustments") added in MekTools' panel with two buttons.


### Credits:
- lmcintyre for ZoneFbx (https://github.com/lmcintyre/ZoneFbx).
- zwansanwan for manually extracting and organizing all available zones (https://www.nexusmods.com/finalfantasy14/mods/1709).
- all credit for MekTools goes to Meku Arts (https://discord.gg/98DqcKE - 18+ server).
