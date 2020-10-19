from flask import Blueprint, url_for
from pybo.models import Question
from werkzeug.utils import redirect
#app.route를 기능이 추가됄때마다 라우트함수를 추가해야하는데 이것을 블루프린트로 해결
bp = Blueprint('main',__name__,url_prefix='/')#blueprint생성 처음부터 이름,모듈명,url프리픽스 값

@bp.route('/hello') #/hello 접속
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/') #/ 접속
def index():
    return redirect(url_for('question._list'))
    #입력 받은 url 라우트를 역으로 찾아주는 함수 question 함수명이고 _list함수의 등록된 라우트를 추적 list
    # url_for은 /마지막에 인수가 배치됌