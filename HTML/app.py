from application import db, create_app

app = create_app()

if __name__ == "__main__":
    db.create_all(app=create_app())
