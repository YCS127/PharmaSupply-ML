#!/usr/bin/env zsh

# Détection et lancement automatique de Docker Desktop sous WSL2
if ! tasklist.exe 2>/dev/null | grep -i "Docker Desktop.exe" >/dev/null; then
    echo "🚀 Démarrage de Docker Desktop..."
    
    # Chemin standard AppData ou Program Files selon l'installation
    LOCAL_DOCKER="/mnt/c/Users/$USER/AppData/Local/Programs/DockerDesktop/Docker Desktop.exe"
    GLOBAL_DOCKER="/mnt/c/Program Files/Docker/Docker/Docker Desktop.exe"

    if [ -f "$LOCAL_DOCKER" ]; then
        ("$LOCAL_DOCKER" >/dev/null 2>&1 &)
    elif [ -f "$GLOBAL_DOCKER" ]; then
        ("$GLOBAL_DOCKER" >/dev/null 2>&1 &)
    else
        echo "❌ Docker Desktop non trouvé sur Windows."
        exit 1
    fi

    while ! command docker info >/dev/null 2>&1; do
        sleep 1
    done
fi

# Exécution de la commande Docker transmise en arguments
command docker "$@"
