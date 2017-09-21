from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

# 连接表
post_tags = db.Table('post_tags',
                db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
                )

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user_.id'))
    comments = db.relationship('Comment', backref='post', lazy="dynamic")
    # Post 维护多对多的关系
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post> '{}'".format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __repr__(self):
        return '<Tag "{}">'.format(self.title)

    def __init__(self, title):
        self.title = title

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.text[:15])


class User(db.Model):
    __tablename__ = "user_" 
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


from sqlalchemy import func

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()

    top_tags = db.session.query(Tag, func.count(post_tags.c.post_id).label('total')).join(
                post_tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@app.route("/", methods=["GET"])
@app.route("/<int:page>")
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()
            ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
            'home.html',
            posts=posts,
            recent=recent,
            top_tags=top_tags
            )

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
               'post.html',
               post=post,
               tags=tags,
               comments=comments,
               recent=recent,
               top_tags=top_tags
    )

@app.route("/tag/<string:tag_name>")
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
               'tag.html',
               post=post,
               tags=tags,
               recent=recent,
               top_tags=top_tags
    )

@app.route("/user/<string:user_name>")
def user(tag_name):
    user = User.query.filter_by(username=user_name).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
               'user.html',
               post=post,
               recent=recent,
               top_tags=top_tags,
               user=user
    )

if __name__ == '__main__':
    app.run()
