from sqlalchemy.orm import Mapped, mapped_column  # type: ignore
from sqlalchemy import Integer, String, Text  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)
    github_url: Mapped[str] = mapped_column(String(250), nullable=False)
    readme: Mapped[str] = mapped_column(Text, nullable=False)
