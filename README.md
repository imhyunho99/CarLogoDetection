# CarLogoDetection

CarLogoDetection은 업로드된 이미지에서 자동차 로고를 인식하는 웹 서비스입니다.  
PyTorch 기반 모델을 사용하며, Django REST Framework로 API를 제공합니다.  
React를 프론트엔드로 사용하며, Oracle Cloud에서 배포 중입니다.

## 데모

https://carproject.duckdns.org/

---

## 기술 스택

### Backend
- Python
- Django
- Django REST Framework
- PyTorch
- OpenCV

### Frontend
- React (Create React App)

### 배포 및 인프라
- Oracle Cloud Free Tier (Ubuntu 22.04)
- Nginx + uWSGI
- systemd (uWSGI 프로세스 관리)
- SSL 인증: Let's Encrypt (Certbot)

### CI/CD
- GitHub Actions
  - main 브랜치에 push 시 서버로 SSH 접속
  - `deploy.sh` 실행: `git pull → migrate → collectstatic → uWSGI 재시작`

---

## 자동 재학습

- 사용자 피드백 이미지는 `media/feedback_images/`에 저장됩니다.
- 서버는 5분마다 해당 디렉토리를 확인합니다.
- 이미지가 50개 이상이면 자동으로 학습 스크립트가 실행되고 모델이 갱신됩니다.
- 학습 후 사용된 이미지는 자동으로 삭제됩니다.
- 이 자동화는 `cron`과 Python 스크립트로 구성되어 있습니다.

---

## 프로젝트 구조

```bash
CarLogoDetection/
├── carLogoDetection/       # Django 설정 및 루트 URL, WSGI
│   └── ...
├── carLogo/                # 로고 인식 관련 앱
│   ├── views.py
│   ├── models.py
│   ├── utils/
│   │   ├── searchUtils.py
│   │   ├── retrain_replaceUtils.py
│   │   └── auto_retrain.py
│   └── ...
├── media/feedback_images/  # 사용자 피드백 이미지 저장소
├── frontend/               # React 프론트엔드
├── deploy.sh               # 배포 스크립트
├── uwsgi.ini               # uWSGI 설정
└── ...
