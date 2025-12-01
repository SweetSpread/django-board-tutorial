from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 우리가 만든 커스텀 User 모델을 관리자 페이지에 등록
admin.site.register(User, UserAdmin)
