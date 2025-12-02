"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # include imports
from django.conf import settings    # 설정 가져오기
from django.conf.urls.static import static  #정적파일 연결 함수

urlpatterns = [
    path('admin/', admin.site.urls),

    # http://127.0.0.1:8000/board/ 로 시작하는 모든 요청은
    # boards 앱 안에 있는 urls.py 파일로 처리를 넘긴다는 뜻
    path('board/', include('boards.urls')),

    # http://127.0.0.1:8000/accounts/ 로 시작하는 모든 요청은
    # accounts 앱 안에 있는 urls.py 파일로 처리를 넘긴다는 뜻
    path('accounts/', include('accounts.urls')),
]

# 개발 모드일 때만 미디어 파일 서빙 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)