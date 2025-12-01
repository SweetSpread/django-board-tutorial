# redirect : 작업 완료 후 다른 페이지로 튕겨주는 역할(response.sendRedirect)
# login_required : 로그인 안 한 사람은 못 들어오게 막는 어노테이션(Spring Security 설정과 유사)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Board, Post
from .forms import PostForm # 방금 만든 폼 가져오기
from django.contrib import messages # 알림 메시지 띄우기용 (옵션)
from django.core.paginator import Paginator # 페이징 도구
from django.db.models import Q  # OR 조건을 쓰기 위한 도구

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
    paginator = Paginator(posts, 1)

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
    post.views += 1
    post.save()

    # 3. 화면으로 데이터 전달
    context = {
        'board' : board,
        'post' : post
    }
    
    return render(request, 'boards/board_detail.html', context)

@login_required # 로그인이 필수라고 선언(로그인 안 되어 있으면 로그인 페이지로 보냄)
def board_write(request, board_code):
    # 1.  게시판 확인
    board = get_object_or_404(Board, code=board_code)

    # 2. 요청 방식에 따른 분기 (GET vs POST)
    if request.method == 'POST':
        # [POST 요청] : 사용자가 '저장' 버튼을 눌렀을 때
        form = PostForm(request.POST)   # 사용자가 입력한 데이터(request.POST)를 폼에 채워넣음

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
        form = PostForm(request.POST, instance=post)

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