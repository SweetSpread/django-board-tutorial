from django import forms
from .models import Post

# Post 모델을 기반으로 입력 폼을 자동으로 생성하는 클래스
class PostForm(forms.ModelForm):
    class Meta:
        model = Post    # 어떤 모델과 연결할지 지정
        fields = ['title', 'content']   # 사용자에게 입력받을 필드만 지정
        # author(작성자)나 board(게시판)는 코드로 자동 입력할 것이므로 제외합니다.

        # 각 필드에 HTML 속성(class, placeholder 등)을 추가하는 설정
        widgets = {
            'title': forms.TextInput(attrs= {
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '내용을 입력하세요'
            }),
        }