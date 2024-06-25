from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routers.checklist.router import router_checklist
from routers.auth.router import router_auth, get_current_user
from routers.service.router import service_router
from routers.events.router import router_events

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
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    router_auth
)

app.include_router(
    service_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    router_events,
    dependencies=[Depends(get_current_user)]
)


@app.get("/")
async def main():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
