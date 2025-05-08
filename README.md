# 🧠 Guide d’utilisation – Générateur de présence Discord + EXE

## 🔧 Prérequis

1. **Installer Python 3.10 ou supérieur** :
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Installer les dépendances nécessaires** :
   Ouvre un terminal ou un invite de commande et tape :

   ```bash
   pip install pypresence pyinstaller pillow
   ```

---

## 🎮 Créer ton Application Discord

1. Va sur [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique sur **"New Application"**.
3. Donne-lui un nom, puis note **l'Application ID** (copie-colle-le dans le code Python à la place du `CLIENT_ID = "-"`).
4. Dans l’onglet **"Rich Presence" > "Art Assets"** :

   * Ajoute une image carrée **512x512 minimum**.
   * Nomme-la **`logo`** (important pour que ça s’affiche dans Discord).

---

## 🖥️ Lancer le générateur

1. Télécharge (ou clone) le dépôt GitHub contenant ce fichier : `Modification_activite_Discord_invité.py`
2. Ouvre le fichier avec **Python (double-clic ou via un éditeur comme VS Code)**.
3. Une interface s’affiche :

   * **Nom esthétique** : nom du fichier EXE final (optionnel).
   * **Description** : ce qui s'affichera dans ta présence Discord.
   * Tu peux écrire **plusieurs lignes** (elles seront fusionnées et nettoyées).
   * Clique sur :

     * `Générer l'EXE` pour créer un exécutable.
     * `Lancer l'EXE` pour l’ouvrir.
     * `Actualiser Presence` pour changer ce qui est affiché en direct dans Discord.

---

## ✅ Exemple d'utilisation

* Nom esthétique : `IdleMasterClone`
* Description :

  ```
  Je suis en train de farmer
  sur Steam grâce à un bot
  ultra secret 😎
  ```

---

## 🆘 Astuces

* Si Discord n'affiche rien, **redémarre Discord** ou vérifie que ton Application ID est correct.
* Le fichier EXE se trouve dans le dossier `dist/` après la génération.
* Si tu ne vois pas l’image dans Discord, vérifie qu’elle est bien **nommée `logo`** dans l'application Discord Developer.

---
