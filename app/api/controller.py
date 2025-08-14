from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.models.entities import User, Book
from app.db.database import get_session
from app.auth.auth_handler import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
)

router = APIRouter()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session)
):
    user = await authenticate_user(
        form_data.username,
        form_data.password,
        session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=User)
async def create_user(user: User, session=Depends(get_session)):
    user.hashed_password = get_password_hash(user.hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/books/", response_model=Book)
async def create_book(
    book: Book,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    book.owner_id = current_user.id
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


@router.get("/books/", response_model=list[Book])
async def read_books(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    result = await session.execute(select(Book).where(
        Book.owner_id == current_user.id)
    )
    books = result.scalars().all()
    return books


@router.get("/books/{book_id}", response_model=Book)
async def read_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    book = await session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )
    return book


@router.put("/books/{book_id}", response_model=Book)
async def update_book(
    book_id: int,
    book: Book,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    db_book = await session.get(Book, book_id)
    if not db_book or db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )
    db_book.title = book.title
    db_book.author = book.author
    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    db_book = await session.get(Book, book_id)
    if not db_book or db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )
    await session.delete(db_book)
    await session.commit()
    return {"ok": True}
