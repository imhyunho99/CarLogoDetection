#!/bin/bash

# 개발 워크플로우 스크립트
echo "🛠️  CarLogoDetection 개발 워크플로우"
echo "=================================="
echo "1. 전체 동기화 (커밋 포함)"
echo "2. 빠른 동기화 (개발용)"
echo "3. 서버 상태 확인"
echo "4. 서버 로그 확인"
echo "5. 종료"
echo ""

read -p "선택하세요 (1-5): " choice

case $choice in
    1)
        echo "전체 동기화 실행..."
        ./sync_to_server.sh
        ;;
    2)
        echo "빠른 동기화 실행..."
        ./quick_sync.sh
        ;;
    3)
        echo "서버 상태 확인..."
        ./check_server.sh
        ;;
    4)
        echo "서버 로그 확인..."
        ssh -i /Users/nahyeonho/.ssh/deploy_test.key ubuntu@140.245.71.233 "sudo tail -50 /var/log/uwsgi/uwsgi.log"
        ;;
    5)
        echo "종료합니다."
        exit 0
        ;;
    *)
        echo "잘못된 선택입니다."
        exit 1
        ;;
esac
