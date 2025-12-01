from django.urls import path
from . import views # 현재 폴더(.)에 있는 views.py를 가져옴

# URL 네임스페이스(JSP에서 <c:url value='boards:list'> 처럼 쓰기 위함)
app_name = 'boards'

urlpatterns = [
    # 목록 화면
    # 주소 패턴: /board/자유게시판코드/
    # <str:board_code>: 자바의 @PathVariable String boardCode 와 동일
    # URL에 들어온 값을 'board_code'라는 변수에 담아 view로 넘깁니다.
    path('<str:board_code>/', views.board_list, name='board_list'),

    # 상세 화면
    # <int:pk> : 정수형(int) 변수를 받아서 'pk'라는 이름으로 뷰에 넘깁니다.
    # 자바의 @PathVariable int pk 와 같습니다.
    # 예시 URL: /board/free/1/
    path('<str:board_code>/<int:pk>', views.board_detail, name='board_detail'),

    # 등록 화면
    path('<str:board_code>/write/', views.board_write, name='board_write'),

    # 수정 화면(글 번호 pk가 필요)
    path('<str:board_code>/<int:pk>/edit/', views.board_edit, name='board_edit'),

    # 삭제
    path('<str:board_code>/<int:pk>/delete/', views.board_delete, name='board_delete'),
]