from fastapi import FastAPI, Query, HTTPException
import requests

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'subject': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'subject': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'subject': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'subject': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'subject': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'subject': 'math'}]

app = FastAPI(title="📚 Alex's Book Search App")

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

@app.get("/")
def root():
    return {"message": "Welcome, Alex! Use /search?q=your_query to find books."}


@app.get("/search")
def search_books(
    q: str = Query(..., description="Search term (title, author, or subject)"),
    limit: int = Query(5, description="Number of results to return"),
):
    """
    Search books using the Open Library API
    """
    params = {"q": q, "limit": limit}
    response = requests.get(OPEN_LIBRARY_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Open Library API error")

    data = response.json()
    books = []

    for doc in data.get("docs", []):
        title = doc.get("title")
        authors = ", ".join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown Author"
        year = doc.get("first_publish_year", "N/A")
        cover_id = doc.get("cover_i")
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None

        books.append({
            "title": title,
            "author": authors,
            "year": year,
            "cover_url": cover_url,
            "openlibrary_link": f"https://openlibrary.org{doc.get('key')}"
        })

    if not books:
        return {"message": f"No books found for '{q}'"}

    return {"query": q, "results": books}
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param:str):
    return{'dynamic_param':dynamic_param}
