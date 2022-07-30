import os
from fastapi import FastAPI, Response
from deta import Deta

app = FastAPI()
deta = Deta()

client_type = None
dbgSplashpage = f"""

 ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌       ▐░▌▐░▌          ▐░▌          
▐░▌   ▄   ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌ ▐░▌░▌ ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌
▐░▌▐░▌ ▐░▌▐░▌          ▐░▌          ▐░▌
▐░▌░▌   ▐░▐░▌ ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌
▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀       ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                       
Powered by https://Deta.sh


Deta Project:\t{deta.project_id}
Client Type:\t{client_type}
Instance Slug:\t{os.getenv("DETA_PATH")}
Running on Micro:\t{os.getenv("DETA_RUNTIME")}
"""

@app.get("/init")
async def init():
    # Loading animation
    # Redirect to done
    client_type = os.getenv("client_type")
    if client_type is not None:
        return dbgSplashpage
    return Response("Bad request", status_code=400)


@app.get("/config")
async def get_config():
    # Poll DB
    # Retrieve Settings
    # Retrieve Subscriptions
    return "TODO: Make redirect to android intent"


@app.get("/console")
async def showConsole():
    return "TODO"