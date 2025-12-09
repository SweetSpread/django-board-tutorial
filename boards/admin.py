from django.contrib import admin
from .models import Board, Post, Comment

# 게시판(Board) 관리
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'description')  # 목록에 보여줄 컬럼
    list_display_links = ('code', 'title')           # 클릭해서 수정할 수 있는 컬럼

# 게시글(Post) 관리 - 여기가 제일 중요!
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 목록에 보일 항목들 (제목, 작성자, 게시판, 조회수, 작성일)
    list_display = ('title', 'author', 'board', 'views', 'created_at')

    # 우측 필터 사이드바 (게시판별, 작성일별 필터링)
    list_filter = ('board', 'created_at')

    # 상단 검색창(제목, 내용, 작성자 닉네임으로 검색)
    # author__nickname: author(User) 모델의 nickname 필드를 검색하겠다는 뜻
    search_fields = ('title', 'content', 'author__nickname', 'author__username')

    # 날짜 계층 구조 (상단에 연도-월-일 네비게이션 생김)
    date_hierarchy = 'created_at'

    # 페이지당 보여줄 개수
    list_per_page = 20

# 댓글(comment) 관리
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_summary', 'post', 'author', 'created_at')
    search_fields = ('content', 'author__username')

    # 댓글 내용이 길 수 있으니 앞부분만 잘라서 보여주는 함수
    def content_summary(self, obj):
        return obj.content[:20] + "..." if len(obj.content) > 20 else obj.content
    content_summary.short_description = "댓글 내용"

# 관리자 페이지에서 Board(게시판) 테이블을 관리하겠다는 뜻
#admin.site.register(Board)

# 관리자 페이지에서 Post(게시물) 테이블을 관리하겠다는 뜻
#admin.site.register(Post)

# 관리자 페이지에서 comment(댓글) 테이블을 관리하겠다는 뜻
#admin.site.register(Comment)