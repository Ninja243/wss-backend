import os
import secrets
from fastapi import FastAPI, Response, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from deta import Deta

app = FastAPI()
deta = Deta()
security = HTTPBasic()

logo = """
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
                                       
Powered by <a href="https://deta.sh">deta.sh</a>"""

debug_page = f"""
<header>
    <title>WSS Debug Page</title>
</header>
<body><pre style="color:purple;">
{logo}
</pre>

Deta Project:\t\t\t{deta.project_id}
Client Type:\t\t\t{os.getenv("client_type")}
Instance Slug:\t\t\t{os.getenv("DETA_PATH")}
Running on Micro:\t\t\t{os.getenv("DETA_RUNTIME")}

</body>
"""

splash_screen = f"""
<header>
    <title>WSS Debug Page</title>
</header>
<body><pre style="color:purple;">
{logo}
</pre>
<form action="" method="post">
    <button name="foo" value="upvote">Upvote</button>
</form>
</body>
"""

def password_check(credentials: HTTPBasicCredentials = Depends(security)):
    base = deta.Base("wss")
    if secrets.compare_digest(str(base.get("password")), credentials.password):
        return "admin" 
    else:
        raise HTTPException(
            status_code=401,
            detail=f"Incorrect Login {credentials.username} {credentials.password} != {str(base.get('password'))}",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/")
async def splash():
    # Password store
    base = deta.Base("wss")
    try: # TODO hash and salt
        base.insert(key="password", os.getenv("password")) # type: ignore   The env will always be set and even if it's not it will fail gracefully
    except:
        print("[!] Password already set, cannot reset")

    # Loading animation
    # Redirect to done
    return RedirectResponse(f"https://{os.getenv('DETA_PATH')}.deta.dev/init")


@app.get("/init")
async def init(user = Depends(password_check)):
    return Response(debug_page, media_type="text/html")
    # Check if ran first in DB

@app.get("/config")
async def get_config():
    # Poll DB
    # Retrieve Settings
    # Retrieve Subscriptions
    return "TODO: Make redirect to android intent"


@app.get("/console")
async def get_console():
    return "TODO"