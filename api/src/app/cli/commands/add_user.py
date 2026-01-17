from getpass import getpass

from app.core.database import db_session
from app.domains.auth.service import add_user


def register(subparsers):
    parser = subparsers.add_parser("add_user", help="Add user")
    parser.add_argument("--email")
    parser.add_argument("--password")

    def handle(args):
        email = args.email or input("Email: ")
        password = args.password or getpass("Password: ")

        with db_session() as db:
            try:
                user = add_user(db, email, password)
                print(f"✅ User {user.email} - created with ID: {user.id}")
            except Exception as e:
                print(f"❌ Error: {e}")

    parser.set_defaults(func=handle)
