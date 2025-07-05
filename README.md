# 🚗 CarLogoDetection

CarLogo 프로젝트는 업로드된 이미지에서 자동차 로고를 인식하는 AI 기반 웹 서비스입니다. PyTorch 모델을 기반으로 로고를 감지하고, Django + DRF를 통해 API로 제공합니다. 프론트엔드는 React 기반이며, Oracle Cloud에서 호스팅되고 있습니다.

## 🌐 데모 URL

🔗 [http://<your-domain-or-ip>](https://carlogo.duckdns.org)

---

## 🔧 사용 기술 스택

### 📁 Backend
- Python
- Django, Django REST Framework
- PyTorch, OpenCV

### 💻 Frontend
- React (Create React App 기반)

### 🚀 배포 & 인프라
- Cloud: Oracle Cloud Free Tier (Ubuntu 22.04)
- Web Server: Nginx + uWSGI
- WSGI 서비스 관리: `systemd`
- SSL 인증서: Let's Encrypt (Certbot)

### 🔄 CI/CD
- GitHub Actions
  - main 브랜치 push 시 서버에 SSH 접속
  - `deploy.sh` 스크립트 실행 (자동 배포)
    - git pull → migrate → collectstatic → uWSGI 재시작

---

## 📂 프로젝트 구조

```bash
CarLogoDetection/
├── carLogoDetection/       # Django 프로젝트 디렉토리
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── carLogo/                # 자동차 로고 인식 앱
│   ├── views.py
│   ├── utils/              # 모델 로딩 및 예측 함수 포함
│   └── ...
├── frontend/               # React 프론트엔드 앱
├── deploy.sh               # 자동 배포 스크립트
├── uwsgi.ini               # uWSGI 설정 파일
└── ...
