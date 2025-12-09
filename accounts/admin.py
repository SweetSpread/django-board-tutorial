from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 목록 화면에서 보이는 컬럼 설정
    # (기본) 아이디, 이메일, 이름, 스태프여부 + (추가) 닉네임, 게시판관리자여부
    list_display = ('username', 'nickname', 'email', 'is_board_manager', 'is_staff', 'is_superuser')

    # 수정 화면(상세)에서 보이는 필드 설정(fieldsets)
    # 기존 UserAdmin의 설정 뒤에 '추가 정보' 섹션을 붙입니다.
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('nickname', 'avatar', 'is_board_manager')}),
    )

# 우리가 만든 커스텀 User 모델을 관리자 페이지에 등록
admin.site.register(User, CustomUserAdmin)
