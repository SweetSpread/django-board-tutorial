from django.urls import path
from django.contrib.auth import views as auth_views # Django가 제공하는 로그인/로그아웃 뷰
from . import views
from .forms import CustomAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    # 회원가입 URL : /accounts/signup/
    path('signup/', views.signup, name='signup'),

    # 로그인
    # as_view(template_name=...): "로직은 Django 것을 쓰되, 화면(HTML)은 내가 만든 걸 보여줘"
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html', 
        authentication_form=CustomAuthenticationForm
        ), name='login'),

    # 로그아웃
    # 로그아웃은 화면이 필요 없으므로 템플릿 지정 안 함
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 프로필 조회(마이페이지)
    path('profile/', views.profile, name='profile'),

    # 프로필 수정
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]