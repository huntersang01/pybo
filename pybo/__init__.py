from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#ORM 라이브러리 참조 DB접속할때 테이플과 매핑된 모델객체를 통해 데이터 처리
import config

db = SQLAlchemy()#ORM라이브러리
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
    migrate.init_app(app, db)
    
    from . import models
    #블루프린트
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    return app
