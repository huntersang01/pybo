from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

from .. import db
from ..models import Question
from ..forms import QuestionForm, AnswerForm
bp = Blueprint('question', __name__, url_prefix='/quesiton')



@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1) #페이지 get방식으로 요청한 url에서 page값 가져올때 사용
    question_list = Question.query.order_by(Question.create_date.desc())
     #order_by는 조회결과를 정렬하는 함수 Question.create_date.desc()는 조회된 데이터를 작성일시 기준으로 역순정렬
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)
        #question/question_list.html 파일을 템플릿 파일이라 부름 템플릿파일을 화면으로 렌더링해줌

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)#해당 데이터 찾지못하면 404페이지 출력
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        #request.method는 현재 요청된 전송방식 의미,form.validate_on_submit()는 post로 전송된 폼데이터 정합성 체크
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now()
        , user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)