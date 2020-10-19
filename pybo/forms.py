from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField#글자수 제한 stringfield,제한없음 textAreafield
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])#validators는 검증도구 datarequired는 필수항목 체크도구
    content = TextAreaField('내용',validators=[DataRequired('내용은 필수입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])