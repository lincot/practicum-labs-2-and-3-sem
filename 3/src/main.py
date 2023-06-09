from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QPlainTextEdit,
    QTableView,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot, QSortFilterProxyModel
import os
import sys
import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    select,
    insert,
    delete,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from alchemy_table import AlchemicalTableModel

import qdarktheme

Base = declarative_base()
engine = create_engine("postgresql://anon:password@localhost/library", future=True)
Session = sessionmaker(bind=engine, future=True)


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        search = self.filterRegExp().pattern()
        model = self.sourceModel()
        for i in range(model.columnCount(sourceParent)):
            index = model.index(sourceRow, i, sourceParent)
            if search in index.data(Qt.DisplayRole):
                return True
        return False


class Language(enum.Enum):
    english = 1
    russian = 2
    ukrainian = 3
    german = 4
    chinese = 5
    japanese = 6


class Book(Base):
    __tablename__ = "books"

    isbn = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    language = Column(Enum(Language))
    issue_year = Column(Integer)


class App:
    def __init__(self):
        self.session = Session()

    def create_book(
        self,
        isbn: str,
        title: str,
        author: str,
        language: Language,
        issue_year: int,
        description: str,
    ):
        self.session.add(
            Book(
                isbn=isbn,
                title=title,
                author=author,
                language=language,
                issue_year=issue_year,
                description=description,
            )
        )
        self.session.commit()

    # def load_books(self):
    #     self.books = self.session.execute(select(Book)).scalars().all()

    def delete_book(self, isbn: int):
        self.session.execute(delete(Book).where(Book.isbn == isbn))
        self.session.commit()

    def create_tab_layout(self):
        layout = QVBoxLayout()

        form = QFormLayout()

        isbn_e = QLineEdit()
        form.addRow("ISBN-13", isbn_e)
        title_e = QLineEdit()
        form.addRow("title", title_e)
        author_e = QLineEdit()
        form.addRow("author", author_e)
        language_e = QLineEdit()
        form.addRow("language", language_e)
        issue_year_e = QLineEdit()
        form.addRow("issue year", issue_year_e)
        description_e = QPlainTextEdit()
        form.addRow("description", description_e)

        layout.addItem(form)

        button = QPushButton("create book")
        button.clicked.connect(
            lambda: self.create_book(
                isbn_e.text(),
                title_e.text(),
                author_e.text(),
                Language[language_e.text()],
                int(issue_year_e.text()),
                description_e.toPlainText(),
            )
        )
        layout.addWidget(button)
        return layout

    def read_tab_layout(self):
        model = AlchemicalTableModel(
            self.session,
            self.session.query(Book),
            [
                (a, b, a, {})
                for (a, b) in (
                    ("isbn", Book.isbn),
                    ("title", Book.title),
                    ("author", Book.author),
                    ("language", Book.language),
                    ("issue_year", Book.issue_year),
                    ("description", Book.description),
                )
            ],
        )

        proxy_model = CustomSortFilterProxyModel()
        proxy_model.setSourceModel(model)

        view = QTableView()
        view.setModel(proxy_model)

        filter_line_edit = QLineEdit()
        filter_line_edit.textChanged.connect(proxy_model.setFilterRegExp)
        layout = QVBoxLayout()
        layout.addWidget(view)
        layout.addWidget(filter_line_edit)

        return layout

    def delete_tab_layout(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        isbn_e = QLineEdit()
        form.addRow("ISBN-13", isbn_e)
        layout.addItem(form)

        button = QPushButton("delete book")
        button.clicked.connect(lambda: self.delete_book(int(isbn_e.text())))

        layout.addWidget(button)

        return layout

    def window(self):
        app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        self.tabs = QTabWidget()
        for layout, name in (
            (self.create_tab_layout(), "create"),
            (self.read_tab_layout(), "read"),
            (self.delete_tab_layout(), "delete"),
        ):
            tab = QWidget()
            tab.setLayout(layout)
            self.tabs.addTab(tab, name)
        self.tabs.show()
        sys.exit(app.exec_())


def main():
    App().window()


if __name__ == "__main__":
    main()
