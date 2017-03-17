from flask import render_template, abort
from . import main
from ..models import BookShelf, Book, Chapter

@main.route('/bs/<int:bookshelf_id>', methods=['GET'])
def load_bookshelf(bookshelf_id):
    pass

@main.route('/b/<int:book_id>', methods=['GET'])
def load_book(book_id):
    pass

@main.route('/c/<int:chapter_id>', methods=['GET'])
def load_chapter(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    if not chapter:
        abort(400)
    return render_template('chapter.html', chapter=chapter)
