from fastapi import FastAPI
from db.db_config import engine
from Models import models
from Router import locations, categories, recommendations

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(locations.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")


