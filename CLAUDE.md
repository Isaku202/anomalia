# Anomalia RPG - Notes de développement

## Accès au projet

- **Dossier local** : `~/Desktop/RPG_Anomalia/projet_rpg/`
- **GitHub** : https://github.com/Isaku202/anomalia
- **Site web** : https://isaku202.github.io/anomalia/
- **Jeu en ligne** : https://isaku202.github.io/anomalia/play/
- **Release** : https://github.com/Isaku202/anomalia/releases/tag/v1.0

## Commandes utiles

```bash
# Se placer dans le projet
cd ~/Desktop/RPG_Anomalia/projet_rpg

# Activer l'environnement Python
source venv/bin/activate

# Lancer le jeu en local
python3 main.py

# Git : voir l'état des fichiers
git status

# Git : préparer + commiter + envoyer
git add fichier.py
git commit -m "description du changement"
git push

# Git : voir l'historique
git log --oneline

# Mettre à jour le zip téléchargeable
rm -f /tmp/anomalia-v1.0.zip
zip -r /tmp/anomalia-v1.0.zip . -x "./venv/*" "./build/*" "./.git/*" ".DS_Store" "*__pycache__*" "./web/*" "./.github/*"
gh release delete v1.0 --yes
gh release create v1.0 /tmp/anomalia-v1.0.zip --title "Anomalia v1.0" --notes "..."
```

## Structure du projet

```
projet_rpg/
├── main.py                  # Point d'entrée (async pour pygbag)
├── .gitignore
├── web/
│   ├── index.html           # Page d'accueil portfolio
│   └── preview.png          # Image de preview
├── .github/workflows/
│   └── deploy.yml           # Build pygbag + deploy GitHub Pages
├── code/
│   ├── config.py            # Détection web/local, paramètres adaptés
│   ├── page_menu.py         # Menu principal (point d'entrée du jeu)
│   ├── game.py              # Boucle de jeu principale
│   ├── map.py               # MapManger, Map, Portail
│   ├── player.py            # Joueur
│   ├── monstre.py           # Monstres (slimes)
│   ├── pnj.py               # PNJ (Léon, Paul) + quêtes
│   ├── character.py         # Classe commune PNJ/monstres
│   ├── animation.py         # Animations du joueur
│   ├── animation_monstre.py # Animations des monstres
│   ├── affichage_pnj.py     # Sprites des PNJ
│   ├── dialogue.py          # Boîte de dialogue
│   ├── inventaire.py        # Inventaire + items
│   ├── interface.py         # Dessin coeurs et potions
│   ├── module_classe.py     # Stats (Personnage, Monstre)
│   ├── musique.py           # Musique + effets sonores
│   ├── coffre.py            # Coffres + drops
│   ├── quete.py             # Système de quêtes
│   ├── Timer.py             # Minuterie
│   ├── LVL_UP.py            # Notification level up
│   ├── drop_monster.py      # Drops des slimes
│   ├── dino_scr.py          # Screamer dino
│   ├── Game_over_dino.py    # Game over lié au dino
│   ├── page_game_over.py    # Game over normal
│   ├── page_stat.py         # Page stats (non utilisée)
│   ├── utils.py             # Fonctions utilitaires (dessiner_texte_contour)
│   └── archive/             # Anciens fichiers (_v1)
├── Map_graph/               # Maps Tiled (.tmx)
├── anomalia_player/         # Sprite sheet joueur
├── PNJ/                     # Sprite sheets PNJ
├── monstre/                 # Sprite sheet monstres
├── objets/                  # Images UI (dialogues, items, etc.)
├── inventaire/              # Image inventaire
├── sons/                    # Fichiers audio (.ogg)
├── pytmx/                   # Lib vendored pour pygbag
├── pyscroll/                # Lib vendored pour pygbag
└── venv/                    # Environnement virtuel Python
```

## Ce qui a été fait

### Rangement bureau
- Bureau organisé en dossiers : RPG_Anomalia, Lettres_motivation, Scolaire, Perso, Temp

### Audit et corrections du code
- [x] Fix coffre.py (héritage Sprite, image, collision, drop d'items)
- [x] Suppression prints de debug
- [x] Fichiers _v1 déplacés dans archive/
- [x] Factorisation dessiner_texte_contour dans utils.py

### Mise en ligne
- [x] Git initialisé + premier commit
- [x] GitHub repo créé (public)
- [x] Code adapté pour pygbag (boucles async, await asyncio.sleep(0))
- [x] Sons convertis MP3 → OGG Vorbis
- [x] Sprite sheets réduites de 50% (mémoire web)
- [x] config.py pour adapter web vs local (zoom, animations, sprite scale)
- [x] GitHub Actions pour build + deploy automatique
- [x] GitHub Pages activé
- [x] Page d'accueil portfolio (synopsis, gameplay, commandes, stack technique)
- [x] Bouton retour + fond noir sur la page du jeu
- [x] Release v1.0 avec zip téléchargeable
- [x] Fix grésillement audio transition menu → jeu

## Ce qui reste à faire

### Bugs techniques
- [ ] Corriger les arguments mutables par défaut (module_classe.py, inventaire.py, map.py)
- [ ] Supprimer page_stat.py (non utilisé) ou le brancher

### Gameplay
- [ ] Affichage visuel du level up (la fonction existe mais n'est pas appelée)
- [ ] Améliorer les coffres (touche pour ouvrir, animation)
- [ ] Potions : moyen d'en récupérer (drops, coffres)
- [ ] Barre d'endurance pour le sprint
- [ ] Diversifier les monstres
- [ ] Plus de maps et de quêtes
- [ ] Énigmes et indices cachés
- [ ] Cinématiques de souvenirs

### Architecture
- [ ] Base de données pour les sauvegardes (position, inventaire, stats, quêtes)
- [ ] Delta time (vitesse indépendante des FPS)
- [ ] Nettoyage : Pnj et Monstre redéfinissent inutilement les méthodes de Character

### Idées futures (du dossier de conception)
- [ ] Page de statistiques du joueur (touche S)
- [ ] Icône d'inventaire
- [ ] Système de magie
- [ ] Quête principale de collecte de fées
- [ ] Plus de PNJ et d'interactions
- [ ] Plus de fins possibles
