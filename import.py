import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('postgres://iyzxosnvirakvx:aa8462466b57b6dd9a0a55a90eef19b45873614d0f3c19b99c4a5a21b8a0edf4@ec2-107-22-228-141.compute-1.amazonaws.com:5432/d7eo12mqipiu42'))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (title, author, year, isbn) VALUES (:title, :author, :year, :isbn)",
        {"title": title, "author": author, "year": year, "isbn": isbn})
       # sumTotal = db.execute ("COUNT(*) FROM books")
       # print(f"Added "sumTotal")

        db.commit()