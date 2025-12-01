from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login # 로그인 처리 함수
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        # [POST] 가입 처리
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # DB에 저장(비밀번호 암호화 자동 처리)

            # 가입 후 바로 로그인 처리(세션 생성)
            auth_login(request, user)

            # 메인 페이지나 게시판 목록으로 이동
            # (아직 메인 페이지가 없으니 일단 자유게시판으로 보냅니다.)
            return redirect('boards:board_list', board_code='free')
    else:
        # [GET] 가입 폼 보여주기
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


# 회원 정보 조회(마이페이지)
@login_required
def profile(request):
    # 화면에 그냥 현재 로그인한 user 정보를 보내주면 됩니다.
    return render(request, 'accounts/profile.html')

# 회원 정보 수정
@login_required
def profile_edit(request):
    if request.method == 'POST':
        # instance=request.user : 현재 로그인된 사용자 정보를 폼에 채워넣고 시작
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile') # 수정 후 마이페이지로 이동
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})
