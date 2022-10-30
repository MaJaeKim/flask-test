from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column( 'user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column( 'question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
    )
answer_voter = db.Table(
    'answer_voter',
    db.Column( 'user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column( 'answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
    )


class Question( db.Model ):   # question table
    id = db.Column( db.Integer, primary_key = True )
    subject = db.Column( db.String(200), nullable = False )
    content = db.Column( db.Text(), nullable = False )
    create_date = db.Column( db.DateTime(), nullable = False )
    user_id = db.Column(db.Integer, db.ForeignKey( 'user.id',\
            ondelete = 'CASCADE'),nullable=False)
    user    = db.relationship( 'User', backref=db.backref('question_set') )
    modify_date = db.Column( db.DateTime(), nullable=True )
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    
class Answer( db.Model ):     # anwer table
    id = db.Column( db.Integer, primary_key = True )
    # ForeignKey 키로 기존 모델을 연결 CASCADE 질문을 삭제하면 답변도 삭제.
    question_id = db.Column( db.Integer, db.ForeignKey( 'question.id', ondelete='CASCADE'))
    # 기존모덱을 참조(relationship) 
    # 역참조 backref 질문에서 답변을 참조/한질문에 여러개의 답변이 있는경우 질문에달린 답변을 참조
    question    = db.relationship('Question', backref=db.backref('answer_set',))

    content     = db.Column( db.Text(), nullable = False )
    create_date = db.Column( db.DateTime(), nullable = False )
    
    user_id = db.Column(db.Integer, db.ForeignKey( 'user.id',\
            ondelete = 'CASCADE'),nullable=False)
    user    = db.relationship( 'User', backref=db.backref('answer_set') )
    modify_date = db.Column( db.DateTime(), nullable=True )
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
   
class User( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    username = db.Column( db.String(150), unique=True, nullable=False)
    password = db.Column( db.String(200), nullable=False)
    email    = db.Column( db.String(120), unique=True, nullable=False)
    
    
class Comment(db.Model):
    id      = db.Column( db.Integer, primary_key = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'user.id', ondelete='CASCADE'),nullable=False)
    user    = db.relationship( 'User', backref=db.backref('comment_set'))
    content = db.Column( db.Text(), nullable=False)
    create_date = db.Column( db.DateTime() , nullable=False)
    modify_date = db.Column( db.DateTime())

    question_id = db.Column( db.Integer, db.ForeignKey( 'question.id', ondelete='CASCADE'), nullable=True)
    question    = db.relationship( 'Question', backref=db.backref( 'comment_set'))
    
    answer_id = db.Column( db.Integer, db.ForeignKey( 'answer.id', ondelete='CASCADE'), nullable=True)
    answer    = db.relationship( 'Answer', backref=db.backref( 'comment_set'))
    

    
