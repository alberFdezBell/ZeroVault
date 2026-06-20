# --- FASE 1: Construcción de la SPA ---
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar manifiestos e instalar dependencias de Node
COPY package.json package-lock.json ./
RUN npm install

# Copiar código fuente y compilar estáticos para producción con Vite
COPY . .
RUN npm run build

# --- FASE 2: Servidor Web de Producción ---
FROM nginx:1.25-alpine AS runner

# Eliminar la configuración por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar los archivos compilados del frontend desde la fase build
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuración de Nginx para SPA (Vue Router)
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]