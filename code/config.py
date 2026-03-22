import sys

# Détecte si on tourne dans le navigateur (WebAssembly) ou en local
WEB = sys.platform == "emscripten"

# Paramètres adaptés selon la plateforme
if WEB:
    MAP_ZOOM = 0.25
    SPRITE_SCALE = 1.75
    ANIM_SPEED = 13
    ANIM_ATK_SPEED = 7
    ANIM_MONSTRE_SPEED = 13
    ANIM_MONSTRE_ATK_SPEED = 12
else:
    MAP_ZOOM = 0.25
    SPRITE_SCALE = 2
    ANIM_SPEED = 50
    ANIM_ATK_SPEED = 25
    ANIM_MONSTRE_SPEED = 50
    ANIM_MONSTRE_ATK_SPEED = 45
