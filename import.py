import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (title, author, year, isbn) VALUES (:title, :author, :year, :isbn)",
        {"title": title, "author": author, "year": year, "isbn": isbn})
       # sumTotal = db.execute ("COUNT(*) FROM books")
        print(f"Added {title} by {author}.")

    db.commit()

    if __name__ == "__main__":
            main()