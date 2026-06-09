# Image Nginx non-root (nginx-unprivileged tourne sur le port 8080 sans privileges root)
FROM nginxinc/nginx-unprivileged:alpine

# Copier nos fichiers frontend dans Nginx (ecrase les fichiers par defaut)
COPY . /usr/share/nginx/html/

# Copier la config Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 8080 (nginx-unprivileged ne peut pas utiliser le port 80)
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8080/ || exit 1