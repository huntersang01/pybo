from datetime import datetime

from flask import Blueprint, url_for,request, render_template, g, flash
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from ..models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))#post방식으로 전달받음
@login_required
def create(question_id):
    form =AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']#post방식으로 전송된 form을 받음
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)#answer_set은 질문의 답변을 의미 질문의 대한 답변 추가
        db.session.commit()#데이터베이스에 추가
        return redirect(url_for('question.detail', question_id=question_id))#답변생성후 상세조회 페이지로 이동
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required