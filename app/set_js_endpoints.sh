#!/bin/bash

# cria gui/config.js com as variáveis do ambiente
mkdir -p gui

echo "window.CONFIG = {"              > gui/config.js
echo "  BROKER_URL: '${BROKER_URL}'," >> gui/config.js
echo "  ENDPOINT_USUARIOS: '${ENDPOINT_USUARIOS}'," >> gui/config.js
echo "  ENDPOINT_LOCAIS: '${ENDPOINT_LOCAIS}'," >> gui/config.js
echo "  ENDPOINT_RESERVAS: '${ENDPOINT_RESERVAS}'," >> gui/config.js
echo "  ENDPOINT_IMAGENS: '${ENDPOINT_IMAGENS}'" >> gui/config.js
echo "};" >> gui/config.js


# roda o cliente
uvicorn client:app --host 0.0.0.0 --port 8000
