# Installer nvm si pas déjà installé
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recharger le terminal
source ~/.bashrc

# Installer Node.js 20 LTS (recommandé pour Angular 17)
nvm install 20

# Utiliser Node.js 20
nvm use 20

# Vérifier la version
node -v  # Devrait afficher v20.x.x
npm -v   # Devrait afficher 10.x.x

# Rendre cette version par défaut
nvm alias default 20
