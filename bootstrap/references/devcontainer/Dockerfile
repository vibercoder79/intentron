# Code-Crash optionales Toolchain-Image (BOO-81).
# Reproduzierbare Toolchain fuer Team-Setups — macht "Tools einmal installieren"
# (HANDBUCH Anhang S) portabel: jeder Operator bekommt identische Linter/Tools,
# kein "works on my machine". OPTIONAL — System-Install bleibt der Default-Pfad.
#
# Bewusst schlank: Node + Python Basis, dazu die Code-Crash-Standard-Toolchain.
# Versionen anpassen wie es das Projekt braucht.
FROM mcr.microsoft.com/devcontainers/base:debian

# --- System-Pakete ---------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
      git jq curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --- Node (fuer ESLint/Prettier-basierte Projekte) -------------------------
# Das base-Image bringt nvm mit; node LTS aktivieren.
ARG NODE_VERSION=lts/*
RUN su vscode -c ". /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} && nvm alias default ${NODE_VERSION}"

# --- Python-Toolchain via pipx (isoliert, kein Versions-Clash) -------------
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv pipx \
    && rm -rf /var/lib/apt/lists/*
RUN su vscode -c "pipx install semgrep && pipx install ruff"

# --- Globales ESLint (optional; viele Projekte pinnen ESLint lokal) --------
RUN su vscode -c ". /usr/local/share/nvm/nvm.sh && npm install -g eslint"

# Hinweis: SonarScanner / weitere Tools projektspezifisch ergaenzen.
# Die Skills lesen .claude/environment.json — generate-environment-json.sh
# erkennt die hier installierten Tools beim ersten Lauf im Container.
USER vscode
