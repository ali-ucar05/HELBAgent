#!/bin/bash

echo "=== DÉMARRAGE DU SCRIPT D'INSTALLATION ==="

# Vérification/installation CURL
echo "[1/10] Vérification de CURL..."
if ! command -v curl > /dev/null 2>&1; then
    echo "➡ curl n'est pas installé. Installation..."
    if command -v apt > /dev/null 2>&1; then
        sudo apt update
        sudo apt install -y curl
    fi
else
    echo "✔ curl déjà installé."
fi

# Django
echo "[2/10] Vérification de Django..."
if ! pip3 show Django > /dev/null 2>&1; then
    echo "➡ Installation de Django..."
    pip3 install Django
else
    echo "✔ Django déjà installé."
fi

# crispy-forms
echo "[3/10] Vérification de django-crispy-forms..."
if ! pip3 show django-crispy-forms > /dev/null 2>&1; then
    echo "➡ Installation de django-crispy-forms..."
    pip3 install django-crispy-forms
else
    echo "✔ django-crispy-forms déjà installé."
fi

# crispy-bootstrap4
echo "[4/10] Vérification de crispy_bootstrap4..."
if ! pip3 show crispy_bootstrap4 > /dev/null 2>&1; then
    echo "➡ Installation de crispy_bootstrap4..."
    pip3 install crispy_bootstrap4
else
    echo "✔ crispy_bootstrap4 déjà installé."
fi

# Pillow
echo "[5/10] Vérification de Pillow..."
if ! pip3 show Pillow > /dev/null 2>&1; then
    echo "➡ Installation de Pillow..."
    pip3 install Pillow
else
    echo "✔ Pillow déjà installé."
fi

# groq
echo "[6/10] Vérification du module groq..."
if ! pip3 show groq > /dev/null 2>&1; then
    echo "➡ Installation de groq..."
    pip3 install groq
else
    echo "✔ groq déjà installé."
fi

# transformers
echo "[7/10] Vérification du module transformers..."
if ! pip3 show transformers > /dev/null 2>&1; then
    echo "➡ Installation de transformers..."
    pip3 install transformers
else
    echo "✔ transformers déjà installé."
fi

# ollama (Python)
echo "[8/10] Vérification du module Python ollama..."
if ! pip3 show ollama > /dev/null 2>&1; then
    echo "➡ Installation du module Python ollama..."
    pip3 install ollama
else
    echo "✔ ollama (Python) déjà installé."
fi

# Vérification/installation Ollama logiciel
echo "[9/10] Vérification du logiciel Ollama..."
if ! command -v ollama > /dev/null 2>&1; then
    echo "➡ Ollama n'est pas installé. Installation..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✔ Ollama déjà installé."
fi

# Vérification du modèle smollm2:135m
echo "[10/10] Vérification du modèle smollm2:135m..."
if ! ollama list | grep -q 'smollm2:135m'; then
    echo "➡ Téléchargement du modèle smollm2:135m..."
    ollama pull smollm2:135m
else
    echo "✔ Modèle smollm2:135m déjà présent."
fi

echo "=== LANCEMENT DU SERVEUR DJANGO ==="
python3 manage.py runserver
