from fastapi import FastAPI
from app.routers import summary_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    import pandas as pd
    try:
        df = pd.read_csv('./app/sales_data.csv')
        app.state.df = df
        yield
    except FileNotFoundError as e:
        print(f"Error: {e}")
        

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(summary_router, prefix="")
    return app
