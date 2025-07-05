#!/bin/bash

APP_DIR="/home/ubuntu/CarLogoDetection/carLogoDetection"
VENV="/home/ubuntu/carlogo"

cd $APP_DIR

echo "📥 Git pull"
git pull origin master

echo "📦 가상환경 활성화"
source $VENV/bin/activate

echo "📂 Migration & Static"
python manage.py migrate

echo "♻️ 무중단 리로드"
touch  /home/ubuntu/CarLogoDetection/reload.txt

echo "🔄 uWSGI 재시작 (systemd)"
sudo systemctl restart uwsgi

echo "✅ 배포 완료"

