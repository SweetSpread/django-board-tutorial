from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login # 로그인 처리 함수
from .forms import CustomUserCreationForm, CustomUserChangeForm, MessageForm
from django.contrib.auth import get_user_model  # User 모델 가져오기
from django.utils import timezone   # 시간 기록용
from django.contrib.auth.decorators import login_required
from .models import Message # Message 모델 import

def signup(request):
    if request.method == 'POST':
        # [POST] 가입 처리
        form = CustomUserCreationForm(request.POST, request.FILES)
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
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile') # 수정 후 마이페이지로 이동
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


# MESSAGE #
# 1. 쪽지함 (목록)
@login_required
def message_list(request):
    # 받은 쪽지 (나에게 온 것)
    received_messages = Message.objects.filter(receiver=request.user)
    # 보낸 쪽지(내가 보낸 것)
    sent_messages = Message.objects.filter(sender=request.user)

    # 안읽은 쪽지 개수 계산 (read_at이 null인 것만 카운트)
    unread_count = received_messages.filter(read_at__isnull=True).count()

    context = {
        'received_messages': received_messages,
        'unread_count': unread_count,
        'sent_messages': sent_messages,
    }

    return render(request, 'accounts/message_list.html', context)

# 2. 쪽지 상세 보기 & 읽음 처리
@login_required
def message_detail(request, message_pk):
    # 쪽지 객체 가져오기 (없으면 404)
    message = get_object_or_404(Message, pk=message_pk)

    # [권한 체크] 보낸 사람도 아니고, 받은 사람도 아니면 볼 수 없음
    if request.user != message.sender and request.user != message.receiver:
        # 에러 페이지로 보내거나 목록으로 튕겨냄
        return redirect('accounts:message_list')
    
    # [읽음 처리] 받는 사람이 처음 열어본 경우에만 기록
    if request.user == message.receiver and not message.read_at:
        message.read_at = timezone.now()  # 현재 시간 기록
        message.save()

    return render(request, 'accounts/message_detail.html', {'message': message})


# 3. 쪽지 보내기
@login_required
def message_send(request, receiver_pk):
    User = get_user_model()
    receiver = get_object_or_404(User, pk=receiver_pk)

    # [방어 로직] 나 자신에게 보내는 것 방지 (선택사항)
    if receiver == request.user:
        return redirect('accounts:message_list')    # 혹은 에러 메시지 표시
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user   # 보낸 사람 : 나
            message.receiver = receiver # 받는 사람: 지정된 유저
            message.save()
            return redirect('accounts:message_list')
    else:
        form = MessageForm()
    
    return render(request, 'accounts/message_send.html', {'form': form, 'receiver': receiver})