from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routers.checklist_api.router import router_checklist
from routers.auth.router import router_auth
from routers.service.router import service_router
from routers.checklist_api.events.router import router_events

import uvicorn

app = FastAPI(
    title='CheckListService'
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router_checklist,
    prefix='/api',
    tags=['CheckList_api']
)

app.include_router(
    router_auth
)

app.include_router(
    service_router,
    prefix='/service'
)

app.include_router(
    router_events
)


@app.get("/")
async def main():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
