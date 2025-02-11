from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import user, auth, post, comment
from app.database import init_db
from .database import get_db, engine

# post.Base.metadata.create_all(bind = engine)
# comment.Base.metadata.create_all(bind = engine)
# u2.Base.metadata.create_all(bind = engine)



app = FastAPI()

init_db()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Blog!"}

# @app.get("/db-check")
# def check_db_connection(db: Session = Depends(get_db)):
#     return {"message": "Database connection successful"} 

@app.get("/db-check")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  # Run a simple SQL query
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}