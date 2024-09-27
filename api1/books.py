from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Apple", "author": "Mukesh", "category": "Food"},
    {"title": "Bat", "author": "Rakesh", "category": "Sports"},
    {"title": "Cat", "author": "Mahesh", "category": "Animals"},
    {"title": "Donut", "author": "Kristin", "category": "Food"},
    {"title": "Eye", "author": "Sona", "category": "Humans"},
    {"title": "Fish", "author": "Gorge", "category": "Food"}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{type}/{book_info}")
async def read_book(type: str, book_info: str):
    result = []
    for book in BOOKS:
        match type:
            case type if type.lower() == "title":
                if book.get('title').lower() == book_info.lower():
                    result.append(book)
            case type if type.lower() == "author":
                if book.get('author').lower() == book_info.lower():
                    result.append(book)
            case type if type.lower() == "category":
                if book.get('category').lower() == book_info.lower():
                    result.append(book)

    return result


@app.get("/books/")
async def read_category_by_query(category: str):
    result = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            result.append(book)
        else:
            result = f"No Book found with given category"

    return result


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)

