#!/usr/bin/env bash
# Deploys MAAT ETC on a Debian/Ubuntu host: Nginx -> Gunicorn (systemd) -> Flask.
# Usage: sudo ./deploy.sh [repo_root]   (defaults to /vagrant inside the Vagrant VM)
set -euo pipefail

REPO_ROOT="${1:-/vagrant}"
APP_DIR=/var/www/MAATETC
APP_USER="${APP_USER:-vagrant}"

echo "==> Installing system packages"
apt-get update -y
apt-get install -y python3 python3-venv python3-pip nginx rsync

echo "==> Copying application to ${APP_DIR}"
mkdir -p "${APP_DIR}"
rsync -a --delete --exclude 'venv/' --exclude '__pycache__/' "${REPO_ROOT}/files/MAATETC/" "${APP_DIR}/"

echo "==> Creating virtualenv and installing dependencies"
python3 -m venv "${APP_DIR}/venv"
"${APP_DIR}/venv/bin/pip" install --upgrade pip
"${APP_DIR}/venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

chown -R "${APP_USER}:www-data" "${APP_DIR}"

echo "==> Installing systemd unit"
cp "${REPO_ROOT}/files/conf/flask_app.service" /etc/systemd/system/flask_app.service
sed -i "s/^User=.*/User=${APP_USER}/" /etc/systemd/system/flask_app.service
systemctl daemon-reload
systemctl enable --now flask_app
systemctl restart flask_app

echo "==> Configuring Nginx"
cp "${REPO_ROOT}/files/conf/MAATETC.conf" /etc/nginx/sites-available/MAATETC.conf
ln -sf /etc/nginx/sites-available/MAATETC.conf /etc/nginx/sites-enabled/MAATETC.conf
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> Done. MAAT ETC is served by Nginx on port 80."
