#!/usr/bin/env bash
# Script para evitar que Claude o IA aparezcan como contribuidor en Git / GitHub

set -e

echo "=== Configurando Git para excluir a Claude de contribuidores ==="

# 1. Asegurar repositorio Git
if [ ! -d ".git" ]; then
  git init
  echo "✔ Repositorio Git inicializado."
fi

# 2. Configurar autor propio
CURRENT_NAME=$(git config user.name 2>/dev/null || echo "")
CURRENT_EMAIL=$(git config user.email 2>/dev/null || echo "")

if [ -z "$CURRENT_NAME" ] || [ -z "$CURRENT_EMAIL" ]; then
  read -p "Ingresa tu nombre para los commits: " GIT_NAME
  read -p "Ingresa tu correo de GitHub: " GIT_EMAIL
  git config user.name "$GIT_NAME"
  git config user.email "$GIT_EMAIL"
  echo "✔ Autor configurado como: $GIT_NAME <$GIT_EMAIL>"
else
  echo "✔ Autor actual: $CURRENT_NAME <$CURRENT_EMAIL>"
fi

# 3. Ignorar archivos de configuración de Claude
if ! grep -q "^\.claude" .gitignore 2>/dev/null; then
  printf "\n# Ignorar configuraciones de Claude\n.claude/\n.claude\n" >> .gitignore
  echo "✔ Carpeta .claude/ agregada a .gitignore"
fi

# 4. Instalar hook para borrar automáticamente cualquier 'Co-authored-by: Claude'
mkdir -p .git/hooks

cat << 'EOF' > .git/hooks/prepare-commit-msg
#!/usr/bin/env bash
# Elimina cualquier linea de coautoría de Claude o Anthropic
COMMIT_MSG_FILE=$1
if [ -f "$COMMIT_MSG_FILE" ]; then
  sed -i '/[Cc]o-authored-by:.*[Cc]laude/d' "$COMMIT_MSG_FILE"
  sed -i '/[Cc]o-authored-by:.*[Aa]nthropic/d' "$COMMIT_MSG_FILE"
fi
EOF

chmod +x .git/hooks/prepare-commit-msg
echo "✔ Hook instalado en .git/hooks/prepare-commit-msg (bloquea Co-authored-by de Claude)"

echo ""
echo "¡Todo listo! Tus commits solo llevarán tu usuario y Claude no saldrá en los contribuidores de GitHub."
