from django.contrib import admin
from .models import Board, Post, Comment

# 관리자 페이지에서 Board(게시판) 테이블을 관리하겠다는 뜻
admin.site.register(Board)

# 관리자 페이지에서 Post(게시물) 테이블을 관리하겠다는 뜻
admin.site.register(Post)

# 관리자 페이지에서 comment(댓글) 테이블을 관리하겠다는 뜻
admin.site.register(Comment)