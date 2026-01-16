#!/bin/bash

SSH_KEY="/Users/nahyeonho/.ssh/deploy_test.key"
SERVER="ubuntu@140.245.71.233"

echo "🔍 서버 모니터링 시작 - $(date)"
echo "=================================="

# 실시간 모니터링 함수
monitor_resources() {
    echo "📊 시스템 리소스 모니터링 (10초 간격, Ctrl+C로 중단)"
    
    while true; do
        ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SERVER" << 'EOF'
echo "$(date '+%H:%M:%S') | CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)% | MEM: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}') | SWAP: $(free | grep Swap | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
EOF
        sleep 10
    done
}

# 트래픽 모니터링
monitor_traffic() {
    echo "🌐 실시간 트래픽 모니터링"
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SERVER" "sudo tail -f /var/log/nginx/access.log | grep --line-buffered -E '(POST|GET)'"
}

# 서비스 상태 체크
check_services() {
    echo "🔧 서비스 상태 확인"
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SERVER" << 'EOF'
echo "=== uWSGI 상태 ==="
systemctl is-active uwsgi && echo "✅ uWSGI 실행 중" || echo "❌ uWSGI 중단"

echo -e "\n=== Nginx 상태 ==="
systemctl is-active nginx && echo "✅ Nginx 실행 중" || echo "❌ Nginx 중단"

echo -e "\n=== 프로세스 확인 ==="
ps aux | grep -E "(uwsgi|nginx)" | grep -v grep | wc -l | xargs echo "실행 중인 프로세스:"

echo -e "\n=== 포트 확인 ==="
ss -tlnp | grep -E "(80|443)" | wc -l | xargs echo "열린 웹 포트:"

echo -e "\n=== 최근 에러 로그 ==="
sudo tail -5 /var/log/nginx/error.log 2>/dev/null || echo "에러 로그 없음"
EOF
}

# 성능 벤치마크
performance_test() {
    echo "⚡ 성능 테스트 실행"
    
    # 응답 시간 측정
    echo "응답 시간 측정 (5회):"
    for i in {1..5}; do
        response_time=$(curl -o /dev/null -s -w "%{time_total}" https://carproject.duckdns.org)
        echo "  $i: ${response_time}초"
    done
    
    # 동시 접속 테스트
    echo -e "\n동시 접속 테스트 (10개 요청):"
    time curl -s https://carproject.duckdns.org &
    time curl -s https://carproject.duckdns.org &
    time curl -s https://carproject.duckdns.org &
    wait
}

# 메뉴
case "$1" in
    "resources")
        monitor_resources
        ;;
    "traffic")
        monitor_traffic
        ;;
    "services")
        check_services
        ;;
    "performance")
        performance_test
        ;;
    *)
        echo "사용법: $0 [resources|traffic|services|performance]"
        echo ""
        echo "resources   - 실시간 리소스 모니터링"
        echo "traffic     - 실시간 트래픽 모니터링"
        echo "services    - 서비스 상태 확인"
        echo "performance - 성능 테스트"
        ;;
esac
