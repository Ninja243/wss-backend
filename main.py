import os
from fastapi import FastAPI, Response
from deta import Deta

app = FastAPI()
deta = Deta()

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
                                       
Powered by https://deta.sh


Deta Project:\t{deta.project_id}
Client Type:\t{os.getenv("client_type")}
Instance Slug:\t{os.getenv("DETA_PATH")}
Running on Micro:\t{os.getenv("DETA_RUNTIME")}
"""

@app.get("/")
async def init():
    # Password check
    # Loading animation
    # Redirect to done
    return dbgSplashpage


@app.get("/config")
async def get_config():
    # Poll DB
    # Retrieve Settings
    # Retrieve Subscriptions
    return "TODO: Make redirect to android intent"


@app.get("/console")
async def showConsole():
    return "TODO"