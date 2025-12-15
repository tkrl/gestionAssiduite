# 🎯 Projet de Gestion d'Assiduité

Application web professionnelle pour la gestion de présence aux événements avec système de QR codes temporels.

## ✨ Fonctionnalités

- **Calendrier interactif** avec FullCalendar.js
- **Gestion d'événements** (création, modification, suppression)
- **Système d'inscription** avec confirmation par l'organisateur
- **Génération de QR codes** valides uniquement pendant l'événement
- **Scan de présence** (entrée/sortie)
- **Interface moderne** avec Tailwind CSS
- **Double rôle** : utilisateurs peuvent être organisateurs ET participants

## 🚀 Installation

### Prérequis
- Python 3.8+
- PostgreSQL (ou SQLite pour le développement)
- Git

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/tkrl/gestionAssiduite.git
cd gestionAssiduite

python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Pour PostgreSQL (recommandé en production)
# Configurer les variables dans .env puis :
python manage.py migrate

# Pour SQLite (développement)
# Le fichier db.sqlite3 sera créé automatiquement

python manage.py createsuperuser

python manage.py runserver

teamProject/
├── teamProject/  # Configuration Django
├── core/               # Application principale
├── users/              # Application utilisateurs
├── theme/          # Templates de base et fontThène
├── calender/             # Gestion du calendrier
└── requirements.txt    # Dépendances Python

Base de données
Le projet supporte :

PostgreSQL (production) via psycopg2


