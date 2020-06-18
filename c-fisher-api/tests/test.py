from app.app import create_app
from app.models.book import Book
from lin.db import db
from lin.core import User, Group, Auth

app = create_app()
with app.app_context():
    with db.auto_commit():
        group = Group()
        group.name = '普通分组'
        group.info = '就是一个分组而已'
        db.session.add(group)
        db.session.flush()

        user = User()
        user.nickname = 'pedro'
        user.password = '123456'
        user.email = '123456780000@qq.com'
        db.session.add(user)

        auth = Auth()
        auth.auth = '删除图书'
        auth.module = '图书'
        auth.group_id = group.id
        db.session.add(auth)