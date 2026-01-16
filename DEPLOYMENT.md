# 배포 파이프라인 가이드

이 프로젝트는 Oracle Cloud 서버와 연동된 배포 파이프라인을 제공합니다.

## 🚀 사용 방법

### 1. 통합 워크플로우 (권장)
```bash
./dev_workflow.sh
```
메뉴에서 원하는 작업을 선택할 수 있습니다.

### 2. 개별 스크립트 실행

#### 전체 동기화 (커밋 포함)
```bash
./sync_to_server.sh
```
- 로컬 변경사항을 Git에 커밋
- 서버로 파일 동기화
- 서버에서 배포 실행

#### 빠른 동기화 (개발용)
```bash
./quick_sync.sh
```
- 커밋 없이 즉시 동기화
- uWSGI 리로드만 실행

#### 서버 상태 확인
```bash
./check_server.sh
```
- 시스템 상태, 서비스 상태, 로그 확인

## 📁 동기화 제외 파일
- `venv/` - 가상환경
- `.git/` - Git 메타데이터
- `__pycache__/` - Python 캐시
- `.idea/` - IDE 설정
- `media/feedback_images/` - 사용자 피드백 이미지

## 🔧 서버 정보
- **주소**: ubuntu@140.245.71.233
- **SSH 키**: /Users/nahyeonho/.ssh/deploy_test.key
- **원격 디렉토리**: /home/ubuntu/CarLogoDetection
- **서비스 URL**: https://carproject.duckdns.org/

## ⚠️ 주의사항
- 배포 스크립트들은 `.gitignore`에 포함되어 Git에 커밋되지 않습니다
- SSH 키 파일의 권한이 올바른지 확인하세요: `chmod 600 ~/.ssh/deploy_test.key`
- 서버의 uWSGI와 Nginx 서비스가 실행 중인지 확인하세요
