from django.db import models
from django.contrib.auth.models import AbstractUser

# 자바의 'MemberEntity extends BaseUser'와 유사합니다.
# Spring의 Member Entity와 같습니다.
# Django(AbstractUser) 기본 User 모델(ID, PW, email 등)을 상속받고 필요한 필드만 추가합니다.
class User(AbstractUser):
    #추가로 필요한 컬럼만 정의하면 됩니다.

    # 게시판 관리자 여부 (True면 게시판 관리자 권한)
    # default=False: 가입 시 기본값은 일반 사용자
    is_board_manager = models.BooleanField(default=False, verbose_name="게시판 관리자 여부")

    # 추후 닉네임이나 전화번호 등이 필요하면 여기에 추가합니다.
    # 저는 닉네임을 추가하지만, 사용하지 않을 경우 주석 처리 하면 됩니다.
    nickname = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="닉네임")

    # 프로필 사진
    # blank=True: 사진 없이도 가입/수정 가능
    avatar = models.ImageField(upload_to='accounts/avatar/%Y/%m/%d/', blank=True, null=True, verbose_name="프로필 사진")

    def save(self, *args, **kwargs):
        # 만약 닉네임이 비어있다면
        if not self.nickname:
            self.nickname = self.username   # 아이디를 닉네임으로 설정
        super().save(*args, **kwargs)       # 진짜 저장 실행

    def __str__(self):
        # 객체를 출력할 때 아이디(username)가 나오도록 설정(자바의 toString()과 동일)
        # 변경! 닉네임이 있으면 닉네임 리턴, 없으면 아이디 리턴
        #return self.username
        return self.nickname if self.nickname else self.username