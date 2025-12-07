# redirect : 작업 완료 후 다른 페이지로 튕겨주는 역할(response.sendRedirect)
# login_required : 로그인 안 한 사람은 못 들어오게 막는 어노테이션(Spring Security 설정과 유사)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Board, Post, Comment
from .forms import PostForm, CommentForm # 방금 만든 폼 가져오기
from django.contrib import messages # 알림 메시지 띄우기용 (옵션)
from django.core.paginator import Paginator # 페이징 도구
from django.db.models import Q  # OR 조건을 쓰기 위한 도구
from django.utils import timezone
from datetime import datetime, timedelta, time  # 날짜 계산용

# 메인 페이지
@login_required
def home(request):
    # 1. 내가 쓴 글(최신순 5개)
    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')[:5]

    # 2. 내가 쓴 댓글 (최신순 5개)
    # select_related('post'): 댓글이 달린 게시판 제목도 같이 가져오기 위해 (DB 성능 최적화)
    my_comments = Comment.objects.filter(author=request.user).select_related('post').order_by('-created_at')[:5]

    # 3. 내가 좋아요 한 글(최신순 5개)
    # STEP 4에서 related_name='like_posts'로 설정했었습니다.
    like_posts = request.user.like_posts.all().order_by('-id')[:5]

    # 커뮤니티 현황
    # 1. 전체 게시판 통합 인기글 (조회수 높은 순 TOP 5)
    # (나중에 '좋아요' 순으로 바꾸려면 order_by('-likes)로 변경 가능)
    hot_posts = Post.objects.all().order_by('-views')[:5]

    # 2. 자유게시판(free) 최신글 Top 5
    # 주의: admin 페이지에서 코드가 'free'인 게시판을 먼저 만들어야 에러가 안 납니다.!
    # 만약 게시판이 없다면 빈 리스트로 반환되므로 에러는 안납니다.
    free_posts = Post.objects.filter(board__code='free').order_by('-created_at')[:5]

    context = {
        'my_posts': my_posts,
        'my_comments': my_comments,
        'like_posts': like_posts,
        'hot_posts': hot_posts,
        'free_posts': free_posts,
    }
    
    return render(request, 'home.html', context)

# 자바 Controller 메서드와 동일
# request: 자바의 HttpServletRequest
# board_code: URL에서 넘겨받은 게시판 코드 (예 : 'free')
def board_list(request, board_code):

    # 1. 게시판 정보 가져오기
    # BOARD 테이블에서 code가 board_code인 데이터를 찾습니다.
    # get_objtect_or_404: 데이터가 없으면 404 에러 페이지를 띄워줍니다(예외처리 자동화)
    board = get_object_or_404(Board, code=board_code)

    # 2. 해당 게시판의 글 목록 가져오기(모든 글)
    # Post 테이블에서 board가 위에서 찾은 board인 것만 필터링
    # order_by('-created_at'): 작성일 역순(내림차순) 정렬. 앞에 '-'가 붙으면 DESC
    posts = Post.objects.filter(board=board).order_by('-created_at')

    # 2-1. 검색 로직 추가
    # URL에서 'q'라는 파라미터를 가져옵니다. (예: ?q=안녕)
    q = request.GET.get('q', '')

    if q:
        # 제목(title)에 q가 포함되어 있거나(OR) 내용(content)에 q가 포함된 것 필터링
        #icontains : 대소문자 구별 없이 포함 여부 확인 (SQL의 LIKE %q%)
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

    # 2-2. 페이징 처리
    # URL에서 'page'라는 파라미터를 가져옴 (없으면 기본값 1)
    page = request.GET.get('page', 1)

    # Paginator(데이터전체, 한페이지_개수) : 글을 10개씩 자르겠다는 설정
    paginator = Paginator(posts, 10)

    # page_obj : 요청한 페이지에 해당하는 '진짜 데이터'와 '페이징 정보'가 담긴
    page_obj = paginator.get_page(page)

    # 3. 화면(Template)으로 보낼 데이터 묶기
    # 자바의 ModelMap.addAttribute()와 동일
    context = {
        'board' : board,
        #'posts' : posts
        'posts' : page_obj, # 기존 all_posts 대신 잘린 데이터(page_obj)를 넘깁니다.
        'q': q, # 검색어 템플릿으로 다시 돌려줘야 검색창에 글자가 유지됩니다.
    }

    # 4. HTML 파일 렌더링
    # boards/board_list.html 템플릿에 contet 데이터를 담아서 보냅니다.
    return render(request, 'boards/board_list.html', context)


def board_detail(request, board_code, pk):
    # 1. 게시판 확인(URL의 board_code가 유효한지)
    board = get_object_or_404(Board, code=board_code)

    # 2. 게시글 가져오기
    # Post 테이블에서 id가 pk인 것을 찾습니다.
    # board=board 조건은, 남의 게시판 글을 ID만 바꿔서 접근하는 것을 막기 위합니다.
    post = get_object_or_404(Post, pk=pk, board=board)

    # 2-1 조회수 1 증가 로직
    # 단순하게 새로고침할 때 마다 증가하는 방식입니다.
    # (실무에서는 쿠키나 세션을 이용해 '하루에 1번만' 혹은 작성자는 제외 같은 제한을 둡니다.)
    #post.views += 1
    #post.save()

    # 조회수 증가 로직 (쿠키 사용) 으로 변경
    # 1. 쿠키 이름 정의(예: hitboard_free_15)
    cookie_name = f'hitboard_{board_code}_{pk}'

    # 2. 렌더링 미리 준비 (응답 객체를 만들어야 쿠키를 심을 수 있음)
    response = render(request, 'boards/board_detail.html', {
        'board' : board,
        'post' : post,
        'comments' : post.comments.select_related('author').all(),  # 최적화 포함
        'form' : CommentForm()  #댓글 폼
    })

    # 3. 쿠키 확인: 쿠키가 없을 때만 조회수 증가
    if request.COOKIES.get(cookie_name) is None:
        post.views += 1
        post.save()

        # 4. 쿠키 설정(오늘 밤 자정까지만 유지)
        # 내일 0시 구하기
        tomorrow = datetime.now() + timedelta(days=1)
        midnight = datetime.combine(tomorrow, time.min)
        expires = (midnight - datetime.now()).total_seconds()

        # response에 쿠키 심기 (set_cookie)
        response.set_cookie(cookie_name, 'true', max_age=expires)
    
    """
    # 2-2 댓글 입력 폼을 생성해서 템플릿으로 보냄
    #comment_form = CommentForm()

    # 3. 화면으로 데이터 전달
    context = {
        'board' : board,
        'post' : post,
        'comment_form': comment_form,   # 템플릿에서 {{ comment_form }}으로 쓸 수 있음
    }
    
    return render(request, 'boards/board_detail.html', context)
    """
    return response

@login_required # 로그인이 필수라고 선언(로그인 안 되어 있으면 로그인 페이지로 보냄)
def board_write(request, board_code):
    # 1.  게시판 확인
    board = get_object_or_404(Board, code=board_code)

    # 2. 요청 방식에 따른 분기 (GET vs POST)
    if request.method == 'POST':
        # [POST 요청] : 사용자가 '저장' 버튼을 눌렀을 때
        #첨부파일 추가
        #form = PostForm(request.POST)   # 사용자가 입력한 데이터(request.POST)를 폼에 채워넣음
        form = PostForm(request.POST, request.FILES)

        if form.is_valid(): # 유효성 검사(제목이 비어있는지 등) - Spring 의 @Valid
            # commit = False: DB에 당장 저장하지 말고, 잠시 메모리에만 객체(Post)를 만들어달라는 뜻
            post = form.save(commit=False)

            # 폼에서 입력받지 않은 나머지 데이터(작성자, 게시판)를 코드로 채워넣음
            post.author = request.user  # 현재 로그인한 사용자
            post.board = board  # 현재 게시판

            post.save() # 이제 DB에 INSERT 전송

            # 글 작성 후 상세 페이지로 이동
            return redirect('boards:board_detail', board_code=board.code, pk=post.pk)
    else:
        # [GET 요청] : 사용자가 처음 '글쓰기' 링크를 클릭했을 때
        form = PostForm()   # 빈 폼을 생성
    
    # 3. 화면 렌더링(빈 폼 혹은 에러가 포함된 폼을 전달)
    return render(request, 'boards/board_write.html', {'form' : form, 'board': board})

# 게시글 수정
@login_required
def board_edit(request, board_code, pk):
    board = get_object_or_404(Board, code=board_code)
    post = get_object_or_404(Post, pk=pk, board=board)

    # [권한 체크] 작성자가 아니면 수정 불가
    if post.author != request.user:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('boards:board_detail', board_code=board_code, pk=pk)
    
    if request.method == 'POST':
        #[POST]  수정사항 저장
        # instance=post : 기존 글 데이터를 폼에 채워 넣은 상태에서 수정 시작하겠다는 뜻(핵심!)
        #첨부파일 추가
        #form = PostForm(request.POST, instance=post)
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.update_author = request.user   # 수정자 기록
            post.save()
            return redirect('boards:board_detail', board_code=board_code, pk=post.pk)
    else:
        # [GET] 수정 폼 보여주기
        # instance=post : 기존 DB 데이터를 폼에 자동으로 채워서 보여줌
        form = PostForm(instance=post)

    # 기존 글쓰기 템플릿(board_write.html)을 재사용합니다.
    return render(request, 'boards/board_write.html', {'form': form, 'board': board})

# 게시글 삭제
@login_required
def board_delete(request, board_code, pk):
    board = get_object_or_404(Board, code=board_code)
    post = get_object_or_404(Post, pk=pk, board=board)

    # [권한 체크] 작성자가 아니면 삭제 불가
    if post.author != request.user:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('boards:board_detail', board_code=board_code, pk=pk)
    
    # [실제 삭제] Delete SQL 실행
    post.delete()

    # 삭제 후 목록으로 이동
    return redirect('boards:board_list', board_code=board_code)

# 댓글 저장 기능
@login_required
def comment_create(request, board_code, pk):
    board = get_object_or_404(Board, code=board_code)
    post = get_object_or_404(Post, pk=pk, board=board)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user   # 작성자 : 현재 로그인한 사람
            comment.post = post             # 게시글 : 현재 보고 있는 글
            comment.save()
    
    # 댓글 저장 후 다시 상세 페이지로 리다이렉트
    return redirect('boards:board_detail', board_code=board.code, pk=post.pk)

# 댓글 수정 기능
def comment_edit(request, comment_pk):
    # 수정할 댓글을 DB에서 가져옵니다.
    comment = get_object_or_404(Comment, pk=comment_pk)

    # [보안] 작성자가 아니면 권한 없음 에러를 띄우거나, 원래 페이지로 돌려보냅니다.
    if comment.author != request.user:
        return redirect('boards:board_detail', board_code=comment.post.board.code, pk=comment.post.pk)
    
    if request.method == 'POST':
        # [POST] 수정 내용을 저장할 때
        # instance=comment : 기존에 있던 댓글 데이터를 폼에 채운 상태로 시작 (수정 모드)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # 수정이 끝나면 원래 있던 게시글 상세 페이지로 돌아갑니다.
            return redirect('boards:board_detail', board_code=comment.post.board.code, pk=comment.post.pk)
    else:
        # [GET] 수정 폼을 보여줄 떄
        form = CommentForm(instance=comment)
    
    # 댓글 수정 전용 템플릿을 렌더링합니다.
    return render(request, 'boards/comment_edit.html', {'form': form, 'comment': comment})

# 댓글 삭제 기능
@login_required
def comment_delete(request, comment_pk):
    # 삭제할 댓글을 DB에서 가져옵니다.
    comment = get_object_or_404(Comment, pk=comment_pk)

    # [보안] 작성자 보인 확인
    if comment.author == request.user:
        comment.delete() # DB 에서 삭제
    
    # 삭제 후 원래 있던 게시글 상세 페이지로 돌아갑니다.
    return redirect('boards:board_detail', board_code=comment.post.board.code, pk=comment.post.pk)

@login_required
def post_like(request, board_code, pk):
    post = get_object_or_404(Post, pk=pk)

    # [로직] 좋아요 토글 (Toggle)
    # filter(id=...): 현재 게시글의 좋아요 목록에 내 아이디가 있는지 확인
    if post.likes.filter(id=request.user.id).exists():
        # 이미 눌렀다면 -> 취소 (remove)
        post.likes.remove(request.user)
    else:
        # 안 눌렀다면 -> 추가 (add)
        post.likes.add(request.user)
    
    # 처리가 끝나면 상세 페이지로 다시 이동
    return redirect('boards:board_detail', board_code=board_code, pk=pk)