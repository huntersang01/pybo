from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#ORM 라이브러리 참조 DB접속할때 테이플과 매핑된 모델객체를 통해 데이터 처리
from sqlalchemy import MetaData
from flaskext.markdown import Markdown
import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))#ORM라이브러리
migrate = Migrate()#db 모델을통해 데이터 변경 도와주는 라이브러리
#db 관리 명령
#flask db migrate 모델 신규생성,변경
#flask db upgrade 변경된 내용 적용
def create_app():
    # app = Flask(__name__)만 쓰면 순환참조오류가 발생해 어플리케이션 팩토리 사용 create_app함수 사용한것 
    app = Flask(__name__)
    app.config.from_object(config)
    #ORM
    db.init_app(app)
    Markdown(app, extensions=['nl2br', 'fenced_code'])#줄바꿈 문자br변경,코드표시
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    from . import models
    #블루프린트
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime #datetime 이라는 필터등록

    return app
