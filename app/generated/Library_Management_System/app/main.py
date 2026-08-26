from fastapi import FastAPI

# Import routers
from app.api import auth, books, members, borrow, return_ as return_module, search

app = FastAPI(title="Library Management System")

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(members.router, prefix="/members", tags=["members"])
app.include_router(borrow.router, prefix="/borrow", tags=["borrow"])
app.include_router(return_module.router, prefix="/return", tags=["return"])
app.include_router(search.router, prefix="/search", tags=["search"])
