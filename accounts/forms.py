from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User, Message

# 우리가 설정한 User 모델을 가져옵니다. (AUTH_USER_MODEL)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User    # 이 폼은 우리가 만든 User 모델과 연결됩니다.
        fields = ['username', 'nickname', 'avatar', 'email']  # 입력받을 필드 지정
        # 비밀번호(password)는 UserCreationForm이 알아서 처리해주므로 안 적어도 됩니다.

    # 폼이 생성될 때(__init__) 모든 필드에 반복문을 돌려 css 클래스를 추가합니다.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# 2. 로그인 폼(새로 추가)
# Django 기본 AuthenticationForm을 상속받아 스타일만 입힘.
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User    # 이 폼은 우리가 만든 User 모델과 연결됩니다.
        fields = ['email', 'nickname', 'avatar', 'last_name', 'first_name']  # 입력받을 필드 지정
        # 비밀번호(password)는 UserCreationForm이 알아서 처리해주므로 안 적어도 됩니다.
        
        # [수정] labels 딕셔너리를 이용해 여기서 명시적으로 지정하는 것이 가장 확실합니다.
        labels = {
            'email': '이메일 주소',
            'nickname': '닉네임',
            'avatar': '프로필 사진',
            'last_name': '성',
            'first_name': '이름',
        }

    # 폼이 생성될 때(__init__) 모든 필드에 반복문을 돌려 css 클래스를 추가합니다.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # 라벨을 한글로 변경 (선택사항) - 딕셔너리를 이용하지 않으면 아래 방법으로
        # self.fields['email'].label = "이메일 주소"
        # self.fields['last_name'].label = "성"
        # self.fields['first_name'].label = "이름"

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요.'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '메시지 내용을 입력하세요.'
            })
        }

