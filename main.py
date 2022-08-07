import os
import json
from fastapi import FastAPI, Response, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.hash import bcrypt
from deta import Deta
from enum import Enum
from deta import App

app = App(FastAPI())
#app = FastAPI()
deta = Deta()
security = HTTPBasic()

def getFromBase(key, base=None):
    if base is None:
        base = deta.Base("wss")
    return json.loads(str(base.get(key) or "{}").replace("'", "\"")).get("value")


def password_check(credentials: HTTPBasicCredentials = Depends(security)):
    if bcrypt.verify(credentials.password, getFromBase("Password")):
        return
    else:
        raise HTTPException(
            status_code=401,
            detail=f"Incorrect Login",
            headers={"WWW-Authenticate": "Basic"},
        )


class Client_Type(Enum):
    android = 1
    email = 2
    ios = 3


warnings = ""

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

header = """
<header>
    <title>WSS Debug Page</title>
</header>
"""

loading_page = f"""
{header}
<body><pre style="color:purple;">
Instance starting...
</body>
"""

debug_page = f"""
{header}
<body><pre style="color:purple;">
{logo}

Deta Project:\t\t\t{deta.project_id}
Instance Slug:\t\t\t{os.getenv("DETA_PATH")}
Running on Micro:\t\t{bool(os.getenv("DETA_RUNTIME"))}
Nonce:\t\t\t\t{getFromBase("nonce")}
</pre>

<pre style="color:red;">
{warnings}
</pre>

<p>👉<a href="wss://register_micro?slug={os.getenv("DETA_PATH")}&nonce={str(deta.Base("wss").get("nonce"))}">Click here to register your client with this instance.</a></p>
</body>
"""


@app.get("/")
async def splash(user=Depends(password_check)):
    # This will be the root page
    # Check to see if done with setup first
    base = deta.Base("wss")
    if base.get("init_complete"):
        return Response(debug_page, media_type="text/html")
    return Response(loading_page, media_type="text/html")


@app.post("/register_client")
async def register_client(data: str,  user=Depends(password_check)):
    base = deta.Base("wss")
    stored_nonce = base.get(key="nonce")
    nonce = json.loads(data).get("nonce")
    if nonce == stored_nonce:
        return "TODO: Register notifications"
    raise HTTPException(status_code=403, detail="Nonce doesn't match")


@app.get("/rss")
async def rss(user=Depends(password_check)):
    print("[!] TODO")


@app.lib.cron()
def crawler(event):
    base = deta.Base("wss")
    init_complete = base.get("init_complete")
    if not init_complete:
        try:  
            if os.getenv("Password") is None:
                raise Exception("No password given")
            base.insert(key="Password", data=bcrypt.hash(
                str(os.getenv("Password"))))
            base.insert(key="Subscriptions", data=[])
            base.insert(key="Batch", data=1)
            base.insert(key="Cursor", data=0)
            base.insert(key="Clients", data={})
            base.insert(key="init_complete", data=True)
        except Exception as e:
            print(f"[!] {e}")
    else:
        cursor = getFromBase("Cursor", base)
        clients = getFromBase("Clients", base)
        subscriptions = getFromBase("Subscriptions", base)
        batch = getFromBase("Batch", base)
        if (subscriptions is None) or (clients is None) or (len(subscriptions) < 1) or (len(clients) < 1):
            return "[!] Nothing to do"
        while int(batch) > 0:
            print(f"{subscriptions[cursor % len(subscriptions)]}")
            cursor = cursor + 1
            # Don't let the cursor number get too big
            if cursor > len(subscriptions):
                cursor = cursor - len(subscriptions)
            batch = batch - 1


