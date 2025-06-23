from fastapi import FastAPI
from blog.api.routes import user, post, comment
from blog.api.openapi_tags import openapi_tags

app = FastAPI(
    title="Blog API",
    description="API backend do Blog com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Lázaro Eduardo",
        "email": "lazaro@exemplo.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=openapi_tags
)

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(comment.router, prefix="/comments", tags=["Comments"])
