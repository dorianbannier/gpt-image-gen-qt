# GPT Image Generator

Application de génération d'images via l'API OpenAI (`gpt-image-2`), construite avec PyQt6 pour fonctionner sur **Windows, macOS et Linux**.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green?logo=qt&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--image--2-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/licence-MIT-orange)

---

## Fonctionnalités

- **Génération d'images** à partir d'un prompt texte via `gpt-image-2`
- **Paramètres ajustables** : taille, qualité, format (PNG / JPEG / WebP), fond (transparent / opaque)
- **Sauvegarde** de l'image générée dans le format choisi
- **Clé API** stockée localement (`~/.config/gpt-image-gen/config.json`), jamais transmise ailleurs
- **Interface bilingue** français / anglais, mémorisée entre les sessions
- **Look macOS** : thème clair inspiré des applications native Apple

---

## Captures d'écran

> *À venir*

---

## Installation

### Windows

Télécharge le dernier `.exe` depuis la page [Releases](../../releases) ou l'onglet [Actions](../../actions) → dernier build réussi → **Artifacts**.

Aucune installation requise, double-clique sur `GPT-Image-Generator.exe`.

### Linux / macOS

**Prérequis** : Python 3.11+

```bash
git clone https://github.com/dorianbannier/gpt-image-gen-qt.git
cd gpt-image-gen-qt
./run.sh
```

`run.sh` crée automatiquement un environnement virtuel et installe les dépendances au premier lancement.

### Installation manuelle des dépendances

```bash
pip install PyQt6 openai
python app.py
```

---

## Configuration

Au premier lancement, clique sur **Clé API…** dans la barre d'outils et entre ta clé OpenAI.  
La clé est sauvegardée localement et n'est jamais partagée.

Tu peux obtenir une clé sur [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

---

## Paramètres de génération

| Paramètre | Options | Description |
|-----------|---------|-------------|
| **Taille** | auto, 1024×1024, 1536×1024, 1024×1536 | Résolution de l'image |
| **Qualité** | auto, low, medium, high | Rapport vitesse / qualité |
| **Format** | PNG, JPEG, WebP | Format du fichier de sortie |
| **Fond** | auto, transparent, opaque | Canal alpha (PNG/WebP uniquement) |

---

## Build Windows (développeurs)

Le workflow GitHub Actions génère automatiquement un `.exe` à chaque push sur `main`.

Pour le lancer manuellement : **Actions → Build Windows .exe → Run workflow**

Le build utilise [PyInstaller](https://pyinstaller.org/) en mode single-file (`--onefile`).

---

## Stack technique

- [PyQt6](https://pypi.org/project/PyQt6/) — interface graphique multiplateforme
- [openai](https://pypi.org/project/openai/) — client officiel OpenAI
- [PyInstaller](https://pyinstaller.org/) — packaging Windows
- [GitHub Actions](https://github.com/features/actions) — CI/CD

---

## Licence

MIT — libre d'utilisation, modification et distribution.
