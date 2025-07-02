#!/bin/bash

APP_DIR="/home/ubuntu/CarLogoDetection"
VENV="/home/ubuntu/carlogo"

cd $APP_DIR

echo "📥 Git pull"
git pull origin main

echo "📦 가상환경 활성화"
source $VENV/bin/activate

echo "📂 Migration & Static"
python manage.py migrate
python manage.py collectstatic --noinput

echo "♻️ 무중단 리로드"
touch reload.txt

echo "✅ 배포 완료"

