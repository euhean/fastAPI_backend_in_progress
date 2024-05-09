from fastapi import FastAPI, Depends
from .routers.users import router as users_router
from .routers.meals import router as meals_router
from .internal.admins import router as admins_router
from .dependencies import get_query_token, get_token_header
from .database import Base, engine

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "User",
        "description": "User related endpoints"
    },
    {
        "name": "Admin",
        "description": "Admin related endpoints"
    },
    {
        "name": "Meal",
        "description": "Meal related endpoints"
    }
]

app = FastAPI(dependencies=[Depends(get_query_token)],
              title="BodaOiT API",
              description="BodaOiT API",
              version="2.0",
              docs_url='/docs',
              redoc_url='/redoc',
              openapi_url='/openapi.json',
              openapi_tags=tags_metadata,
              debug=True,
              swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
            )


app.include_router(users_router)
app.include_router(meals_router)
app.include_router(
    admins_router,
    prefix="/admins",
    tags=["Admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)


@app.get("/")
def root():
    return {"message": 'Hello world!'}   