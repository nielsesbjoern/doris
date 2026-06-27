#!/usr/bin/env sh
# Install repo git hooks (pre-commit runs build + diff check).
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="$ROOT/.git/hooks/pre-commit"

cat > "$HOOK" <<'EOF'
#!/usr/bin/env sh
exec "$(git rev-parse --show-toplevel)/scripts/check_build.sh"
EOF

chmod +x "$HOOK"
echo "Installed pre-commit hook → scripts/check_build.sh"
