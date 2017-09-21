from main import app, db, User, Tag, Post
import random
import datetime
user = User.query.get(1)
tag_1 = Tag("Python")
tag_2 = Tag("Perl")
tag_3 = Tag("SQLAlchemy")
tag_4 = Tag("Jinja")

tag_list = [ 
        tag_1,
        tag_2,
        tag_3,
        tag_4
        ]
s = "Example text"

# python3 use range not xrange
for i in range(100):
    new_post = Post("Post" + str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_post.text = s
    new_post.tags = random.sample(tag_list, random.randint(1, 3))
    db.session.add(new_post)

db.session.commit()

