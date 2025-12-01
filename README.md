# 🐍 Django Board Tutorial (Phase 1)

This repository contains the source code for a step-by-step Django web development tutorial. It is designed for Python beginners to learn the core concepts of Django (MVT pattern, ORM, Authentication) by building a fully functional bulletin board service.

이 저장소는 파이썬 입문자를 위한 단계별 Django 웹 개발 튜토리얼 소스코드를 담고 있습니다. 게시판 서비스를 직접 구현하며 Django의 핵심 개념(MVT 패턴, ORM, 인증 등)을 익힐 수 있도록 구성되었습니다.

---

## 🎯 Project Purpose & Goals (목적 및 방향)
* **Step-by-Step Learning:** Code written sequentially from environment setup to deployment-ready features.
* **Core Fundamentals:** Understanding Django's App structure, Model design, and View logic without relying solely on copy-pasting.
* **Practical Features:** Implementing real-world features like CRUD, Pagination, Search, and Authentication.
* **단계별 학습:** 환경 설정부터 기능 구현까지 차근차근 진행되는 과정을 담았습니다.
* **기초 원리 이해:** 단순 복사/붙여넣기가 아닌, Django의 앱 구조, 모델 설계, 뷰 로직을 직접 작성하며 이해하는 것을 목표로 합니다.
* **실무 기능 구현:** CRUD, 페이징, 검색, 회원가입/로그인 등 실제 웹사이트에 필요한 필수 기능을 구현합니다.

---

## 🛠 Features (구현된 기능 - Phase 1)

### 1. Board (게시판)
* **CRUD:** Create, Read, Update, Delete posts (게시글 등록, 조회, 수정, 삭제)
* **Pagination:** List navigation support (페이징 처리)
* **Search:** Search by title or content (제목+내용 검색)
* **View Count:** Hit counter for posts (조회수 증가)

### 2. Authentication (회원 관리)
* **Sign Up & Login:** Custom user model implementation (회원가입 및 로그인)
* **Profile:** My page and profile editing (마이페이지 및 정보 수정)
* **Permission:** Access control for editing/deleting posts (작성자 본인만 수정/삭제 가능)

### 3. UI/UX
* **Bootstrap 5:** Responsive design and modern UI components (부트스트랩 적용)
* **Template Inheritance:** Efficient layout management using `base.html` (템플릿 상속을 통한 레이아웃 관리)

---

## 🚀 How to Run (실행 방법)

If you want to run this project locally, follow these steps:
이 프로젝트를 로컬에서 실행하려면 다음 순서를 따라주세요.

```bash
# 1. Clone the repository
git clone https://github.com/SweetSpread/django-board-tutorial.git
cd django-board-tutorial

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Migrate database
python manage.py migrate

# 5. Create superuser (Admin)
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## 📚 Tutorial & Blog (관련 튜토리얼)

This project is part of a tutorial series documented on my blog. You can find detailed explanations for each step here:
이 프로젝트는 제 블로그에 연재된 튜토리얼의 결과물입니다. 각 단계별 상세한 설명은 아래 링크에서 확인하실 수 있습니다.

👉 **[Step-by-Step Django Tutorial Phase 1](https://try-to-do.tistory.com/category/Step%20by%20Step/%5BPhase%201%5D%20django%20board%20tutorial)**

