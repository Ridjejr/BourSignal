# Étape 1 : On part d'une image Python légère
FROM python:3.13-slim

# Étape 2 : On définit le dossier de travail dans le conteneur
WORKDIR /app

# Étape 3 : On copie d'abord les dépendances (pour le cache Docker)
COPY requirements.txt .

# Étape 4 : On installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : On copie tout le code source
COPY . .

# Étape 6 : On expose le port 5000
EXPOSE 5000

# Étape 7 : On lance le serveur avec gunicorn (production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]