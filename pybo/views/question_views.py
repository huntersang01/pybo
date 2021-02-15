from datetime import datetime

from flask import Blueprint, render_template, request, url_for ,g, flash
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User
from ..forms import QuestionForm, AnswerForm
bp = Blueprint('question', __name__, url_prefix='/quesiton')



@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1) #페이지 get방식으로 요청한 url에서 page값 가져올때 사용
    kw = request.args.get('kw', type=str, default='')

    # 조회
    question_list = Question.query.order_by(Question.create_date.desc())
     #order_by는 조회결과를 정렬하는 함수 Question.create_date.desc()는 조회된 데이터를 작성일시 기준으로 역순정렬
    if kw:

        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \             
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \            
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)
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
        , user=g.user)#form으로 작성한 데이터 전달
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
 #질문수정을 누르면 get 방식으로 돼서 question_form.html을 렌더링 
 # 질문수정 화면에서 저장하기 누르면 post방식으로 밑의 함수실행
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))