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
    nickname = models.CharField(max_length=20, blank=True)

    def __str__(self):
        #객체를 출력할 때 아이디(username)가 나오도록 설정(자바의 toString()과 동일)
        return self.username