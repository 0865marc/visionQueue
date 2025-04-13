#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Ejecutar las migraciones de Alembic
echo "Ejecutando migraciones de la base de datos..."
alembic upgrade head

# Ejecutar el comando principal del contenedor (el CMD del Dockerfile o el command del docker-compose)
echo "Iniciando la aplicación..."
exec "$@"