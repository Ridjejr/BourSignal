# Image Nginx légère
FROM nginx:alpine

# Supprimer la page par défaut de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copier nos fichiers frontend dans Nginx
COPY . /usr/share/nginx/html/

# Copier la config Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80