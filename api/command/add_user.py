from src.database import db_session
from src.auth.service import add_user
from fastapi import HTTPException


def main():
    with db_session() as db:
        try:
            email = input("Email: ")
            password = input("Password: ")
            user = add_user(db, email, password)
            print(f"✅ User created with ID: {user.id}")
        except HTTPException as e:
            print(f"❌ Error: {e.detail}")


if __name__ == "__main__":
    main()
