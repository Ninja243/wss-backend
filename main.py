import os
from fastapi import FastAPI, Response
from deta import Deta

app = FastAPI()
deta = Deta()
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

@app.get("/")
async def splash():
    # Password store
    base = deta.Base("wss")
    try:
        base.insert("password", os.getenv("password")) # type: ignore   The env will always be set and even if it's not it will fail gracefully
    except:
        print("[!] Password already set, cannot reset")

    # Loading animation
    # Redirect to done
    return Response(splash_screen, media_type="text/html")


@app.post("/init")
async def init(password: str):
    base = deta.Base("wss")
    if base.get("password") == password:
        return Response(debug_page, media_type="text/html")
    else:
        return Response("Unauthorized", 403)
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