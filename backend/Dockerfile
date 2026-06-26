# --- Etape 1 : Installation des dependances ---
FROM python:3.13-slim AS builder
WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/build/deps -r requirements.txt


# --- Etape 2 : Image finale (sans les outils de build) ---
FROM python:3.13-slim

# Utilisateur non-root pour la securite
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Recuperer uniquement les librairies compilees depuis le builder
COPY --from=builder /build/deps /usr/local

# Copier le code source (app/, config/, run.py et autres fichiers du projet)
COPY . .

# Dossier partage ou chaque worker Gunicorn ecrit ses metriques
# (necessaire car prometheus_client n'agrege pas en memoire entre processus)
ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc
RUN mkdir -p /tmp/prometheus_multiproc

# Donner les droits a appuser puis basculer dessus
RUN chown -R appuser:appuser /app /tmp/prometheus_multiproc
USER appuser

EXPOSE 5000

# Verifie toutes les 30s que l'API repond. start-period=15s laisse le temps a gunicorn de demarrer.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

CMD ["gunicorn", "-c", "gunicorn.conf.py", "-w", "4", "--preload", "-b", "0.0.0.0:5000", "--access-logfile", "-", "run:app"]