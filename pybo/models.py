from pybo import db


class Question(db.Model):#nullable 비어있는값 들어올수없음 의미 디폴드값은 true
    id = db.Column(db.Integer, primary_key=True)#primary_key 중복 안됌,integer id숫자값
    subject = db.Column(db.String(200), nullable=False)#string제목처럼 제한된 글자수
    content = db.Column(db.Text(), nullable=False)#text글자수 제한 없음
    create_date = db.Column(db.DateTime(), nullable=False)#날짜와 시간
#db.Column 모델클래스 속성 생성
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    #db.ForeignKaey는 다른 모델과의 연결 의미 ,ondelete=cascade는 이 답변과 연결된 질문이 삭제될시 답변도 삭제
    question = db.relationship('Question',backref=db.backref('answer_set'))
    #backref속성은 질문에서 답변모델을 참조하기위해서 사용 
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

 


