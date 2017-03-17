# -*- coding: utf-8 -*-
from app import db

class BookShelf(db.Model):
    __tablename__ = "BookShelf"
    id = db.Column(db.Integer, primary_key=True)
    shelf_name = db.Column(db.String(36))

    def __init__(self, *args, **kwargs):
        super(BookShelf, self).__init__(*args, **kwargs)


class Book(db.Model):
    __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText)
    desc = db.Column(db.UnicodeText)
    auther = db.Column(db.String(32))
    last_chapter_id = db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    last_update_time = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)


class Chapter(db.Model):
    __tablename__ = "Chapter"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    book = db.relationship('Book',
                           foreign_keys=[book_id],
                           backref='chapters')
    title = db.Column(db.UnicodeText)
    content = db.Column(db.UnicodeText)
    prev_chapter_id = db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    next_chapter = db.relationship('Chapter', uselist=False,
                                   backref=db.backref('prev_chapter', remote_side=[id]))

    def __init__(self, *args, **kwargs):
        super(Chapter, self).__init__(*args, **kwargs)
