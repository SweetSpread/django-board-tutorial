from django.shortcuts import render
# 게시판 모델 import
# 보통은 'from boards.models import Post'형식이 됨.
from boards.models import Post

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io
import urllib, base64

import platform
from matplotlib import font_manager, rc

# 1. 운영체제에 맞춰 한글 폰트 설정
if platform.system() == 'Windows':
    # 윈도우인 경우 '맑은 고딕' 사용
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    # 맥(Mac)인 경우 'AppleGothic' 사용
    rc('font', family='AppleGothic')

# 2. 마이너스 기호(-)가 깨지는 현상 방지
plt.rcParams['axes.unicode_minus'] = False

# [추가할 코드 끝] -----------------------------------------
# [Skill 1] 서버 전용 백엔드 설정(GUI 창을 띄우지 않고 파일로만 그림)
plt.switch_backend('Agg')

def dashboard(request):
    '''

    # 1. 데이터 불러오기 (연습용 타이타닉 데이터 사용)
    # (나중에는 myModel.objects.all()로 내 DB 데이터를 가져오면 됌!)
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)

    # ---------------------------------------------------------------
    # [Skill 2] 통계 요약표 만들기(describe)
    # 숫자 데이터들의 통계(개수, 평균, 표준편차, 최소, 최대 등)를 자동으로 뽑아줌
    summary_df = df.describe()

    # DataFrame을 HTML 표 태그(<table>)로 자동 변환해주는 함수
    summary_html = summary_df.to_html(classes='table table-striped')

    # ---------------------------------------------------------------
    # [Skill 3] 데이터 정렬하기 (sort_values)
    # 나이가 많은 순서대로 상위 5명 뽑기
    top_5_oldest = df.sort_values(by='Age', ascending=False).head(5)
    top_5_html = top_5_oldest[['Name', 'Age', 'Pclass']].to_html(classes='table')
    # ---------------------------------------------------------------
    # [Skill 4] 그래프를 그려서 메모리에 저장하기 (파일 저장 X)
    plt.figure(figsize=(10, 6))

    # 원하는 그래프 그리기(예: 등급별 평균 요금)
    sns.barplot(x='Pclass', y='Fare', hue='Sex', data=df)
    plt.title("Fare by Pclass & Sex")

    # 그래프를 이미지 파일로 변환하는 과정(메모리 버퍼 사용)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')   # 버퍼에 그림 저장
    buffer.seek(0)

    # 버퍼의 내용을 글자(Base64 string)로 변환 (HTML이 이해할 수 있게)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # ---------------------------------------------------------------
    # 3. 템플릿으로 보내기
    context = {
        'summary_table': summary_html,  # 통계표 HTML
        'top_5_table': top_5_html,      # 랭킹표 HTML
        'graph_image': graphic,         # 그래프 이미지 데이터
    }

    '''

    # 1. 실제 데이터 DB에서 가져오기
    # author__username: 작성자의 닉네임이나 아이디를 바로 가져오는 ORM 스킬
    posts = Post.objects.all().values('title', 'author__username', 'created_at', 'category')

    # 2. DataFrame으로 변환
    df = pd.DataFrame(posts)

    # [예외 처리] 게시글이 하나도 없으면 에러가 나므로 방어 코드를 짭니다.
    if len(df) == 0:
        return render(request, 'dataAgent/dashboard.html', {'no_data':True})
    
    # ---------------------------------------------------------------
    # [분석 1] 열혈 회원 랭킹 (Top Writers)
    # 'author__username' 컬럼의 값을 세어서(value_counts) 가장 많은 5명 뽑기
    top_writers = df['author__username'].value_counts().head(5)

    #시리즈(Series)를 예쁜 데이터 프레임으로 변환 (표로 보여주기 위해)
    top_writers_df = top_writers.reset_index()
    top_writers_df.columns = ['작성자', '작성글 수']    # 컬럼 이름 한글로 변경
    top_writers_html = top_writers_df.to_html(classes='table table-hover text-center', index=False, justify='center')

    # ---------------------------------------------------------------
    # [분석 2] 일별 게시글 작성 추이(시계열 분석)

    # created_at을 날짜 형식으로 변환(중요 !)
    df['created_at'] = pd.to_datetime(df['created_at'])

    # 'YYYY-MM-DD' 형식의 문자열로 변환해서 'date'라는 새 컬럼 생성
    df['date_str'] = df['created_at'].dt.strftime('%Y-%m-%d')

    # 날짜별로 몇 개의 글이 올라왔는지 세기 (sort_index로 날짜순 정렬)
    daily_counts = df['date_str'].value_counts().sort_index()

    # ---------------------------------------------------------------
    # [분석 3] 카테고리별 점유율 (Pie Chart)

    # 1. 카테고리별 개수 세기
    category_counts = df['category'].value_counts()

    # 2. 영어(DB값) -> 한글(화면용) 변환 사전
    category_map = {
        'common': '일반',
        'question': '질문',
        'review': '후기',
        'notice': '공지'
    }
    # 라벨 리스트 만들기(리스트 내포 문법 사용)
    labels_korean = [category_map.get(cat, cat) for cat in category_counts.index]

    # 3. 파이 차트 그리기
    plt.figure(figsize=(6,6))   # 정사각형 캔버스

    # autopct : 비율 표시 포맷 ('%1.1f%%' -> 소수점 1자리까지)
    # startangle : 시작 각도 (90도=12시방향)
    # colors: Seaborn의 파스텔 톤 색상 팔레트 사용
    plt.pie(category_counts, labels=labels_korean, autopct='%1.1f%%', startangle=90, counterclock=False, colors=sns.color_palette('pastel'))

    plt.title("카테고리별 게시글 비율")

    # 이미지 저장 (인코딩)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_bytes = buffer.getvalue()
    buffer.close()
    graphic_pie = base64.b64encode(img_bytes).decode('utf-8')

    # ---------------------------------------------------------------
    # [시각화] 꺾은선 그래프 그리기 (Line Plot)
    plt.figure(figsize=(10, 5))

    # x축: 날짜, y축 : 개수
    sns.lineplot(x=daily_counts.index, y=daily_counts.values, marker='o', color='coral')

    plt.title("Daily Post Trend")
    plt.xticks(rotation=45) # x축 글씨가 겹치지 않게 45도 기울이기
    plt.grid(True)  # 격자 무늬 추가
    plt.tight_layout()  # 여백 자동 조정

    # 이미지 인코딩
    # 그래프를 이미지 파일로 변환하는 과정(메모리 버퍼 사용)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')   # 버퍼에 그림 저장
    buffer.seek(0)

    # 버퍼의 내용을 글자(Base64 string)로 변환 (HTML이 이해할 수 있게)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # ---------------------------------------------------------------
    # 3. 템플릿으로 전달
    context = {
        'top_writers_table': top_writers_html,
        'daily_trend_graph': graphic,
        'pie_chart': graphic_pie, # <-- 여기 추가되었습니다!
        'total_posts': len(df),
        'no_data': False
    }

    return render(request, 'dataAgent/dashboard.html', context)
