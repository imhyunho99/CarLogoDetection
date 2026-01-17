#!/bin/bash

APP_DIR="/home/ubuntu/CarLogoDetection/carLogoDetection"
VENV="/home/ubuntu/carlogo"

cd $APP_DIR

echo "Creating .env file"
echo "SENTRY_DSN=$SENTRY_DSN" > .env
echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" >> .env

echo "📥 Git pull"
git fetch origin master
git reset --hard origin/master
git pull origin master

echo "Creating logs directory"
mkdir -p logs

echo "📦 가상환경 활성화"
source $VENV/bin/activate

echo "📂 Migration & Static"
python manage.py migrate

echo "♻️ 무중단 리로드"
touch  /home/ubuntu/CarLogoDetection/reload.txt

echo "🔄 uWSGI 재시작 (systemd)"
sudo systemctl restart uwsgi

echo "✅ 배포 완료"


