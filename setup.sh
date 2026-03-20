#!/bin/bash
# ═══════════════════════════════════════════════════
#  JIYA & SHAILESH GALLERY — One-command Setup Script
# ═══════════════════════════════════════════════════

set -e

echo ""
echo " ✨  JIYA & SHAILESH GALLERY — Setup"
echo "─────────────────────────────────────────────"

# 1. Create virtual environment
echo "→  Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "→  Installing dependencies..."
pip install -q -r requirements.txt

# 3. Run migrations
echo "→  Running database migrations..."
python manage.py makemigrations gallery
python manage.py migrate

# 4. Create superuser
echo ""
echo "─────────────────────────────────────────────"
echo "  Create your admin account:"
echo "─────────────────────────────────────────────"
python manage.py createsuperuser

# 5. Collect static (optional for dev)
echo "→  Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo ""
echo "─────────────────────────────────────────────"
echo "✓  Setup complete!"
echo ""
echo "  Start the server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "  Then open:"
echo "  http://127.0.0.1:8000/         ← Public gallery"
echo "  http://127.0.0.1:8000/dashboard/ ← Admin panel"
echo "─────────────────────────────────────────────"
