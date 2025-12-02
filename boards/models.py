from django.db import models
from django.conf import settings # 설정 파일의 AUTH_USER_MODEL을 가져오기 위함

# 1. 게시판 설정 테이블 (예: 공지사항, 자유게시판 등 게시판 '종류'를 관리)
class Board(models.Model):
    # 게시판 이름 (예: 자유게시판)
    title = models.CharField(max_length=100, verbose_name="게시판 이름")

    # URL이나 코드에서 사용할 영문 이름(예: free) - 중복 불가능(unique)
    code = models.CharField(max_length=20, unique=True, verbose_name="게시판 코드")

    # 게시판 설명
    description = models.CharField(max_length=200, blank=True, verbose_name="설명")

    def __str__(self):
        return self.title
    
# 2. 게시판 테이블(실제 글 데이터)
class Post(models.Model):
    # [FK] 어떤 게시판에 속한 글인지 (Board 테이블과 1:N 관계)
    # on_delete = models.CASCADE: 게시판이 삭제되면 글도 다 삭제됨
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="게시판")

    # [FK] 최초 작성자 (User 테이블과 1:N 관계)
    # settings.AUTH_USER_MODEL을 쓰는 것이 Django의 권장 사항입니다.
    # related_name='posts': user.posts 로 이 유저가 '작성한' 글 목록을 가져옴
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name="작성자")

    # [FK] 마지막 수정자
    # null=True: 글 처음 쓸 때는 수정자가 없으므로 DB에 NULL 허용
    # blank=True: 폼 입력 시 비워둬도 됨
    # related_name='updated_posts': user.updated_posts 로 이 유저가 '수정한' 글 목록을 가져옴
    # 주의 : 한 모델에서 User를 2번 이상 참조할 땐 related_name이 필수입니다!
    update_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_posts', null=True, blank=True, verbose_name="수정자")

    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용") # 길이 제한 없는 문자열

    # 생성 시 시간 자동 저장
    # auto_now_add=True: 데이터가 처음 생성될 때 현재 시간 자동 저장
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    # 저장(수정) 될 때마다 시간 자동 갱신
    # auto_now=True: 데이터가 수정될 때 마다 현재 시간 갱신
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="수정일")

    views = models.PositiveBigIntegerField(default=0, verbose_name="조회수")

    # 이미지 필드
    # upload_to='board/images/%Y/%m/%d/': 파일을 저장할 때 '년/월/일' 폴더로 자동 분류해줍니다. (관리용이)
    # blank=True, null=True: 이미지를 첨부하지 않아도 글 작성이 가능하도록 허용합니다.
    image = models.ImageField(upload_to='board/images/%Y/%m/%d/', blank=True, null=True, verbose_name="이미지")

    # 좋아요 (Many-to-Many)
    # User 모델과 다대다 관계를 맺습니다.
    # related_name='like_posts': 나중에 유저 입장에서 "내가 좋아요 누른 글들"을 가져올 때 사용할 이름입니다.
    # (주의: related_name을 안 쓰면 author 필드와 충돌이 날 수 있습니다.)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True, verbose_name="좋아요")

    def __str__(self):
        return f"[{self.board.title}] {self.title}"
    
class Comment(models.Model):
    # [FK] 어떤 게시글에 달린 댓글인지 (Post와 1:N 관계)
    # related_name= 'comments': 나중에 post.comments 로 댓글들을 쉽게 가져오기 위함
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',verbose_name="게시글")

    # [FK] 댓글 작성자
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")

    # 댓글 내용(짧을 수 있으니 TextField 대신 CharField도 가능하지만, 넉넉하게 Text로 갑니다.)
    content = models.TextField(verbose_name="댓글 내용")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return f"[{self.post.title}] {self.content[:20]}..."