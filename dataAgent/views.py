from django.shortcuts import render


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io
import urllib, base64

# [Skill 1] 서버 전용 백엔드 설정(GUI 창을 띄우지 않고 파일로만 그림)
plt.switch_backend('Agg')

def dashboard(request):
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

    return render(request, 'dataAgent/dashboard.html', context)
