from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

from recognize import recognize_faces

app = FastAPI()

# create folders automatically
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

# serve static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/results", StaticFiles(directory="results"), name="results")


# ---------------- LOGIN PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def login_page():

    return """
    <html>
    <head>
    <title>Teacher Login</title>

    <style>

    body{
        font-family: Arial;
        background:#f2f2f2;
        text-align:center;
        padding-top:120px;
    }

    .box{
        background:white;
        padding:40px;
        width:300px;
        margin:auto;
        border-radius:10px;
        box-shadow:0px 0px 10px gray;
    }

    input{
        width:90%;
        padding:10px;
        margin:10px;
    }

    button{
        padding:10px 20px;
        background:#4CAF50;
        color:white;
        border:none;
        cursor:pointer;
    }

    </style>
    </head>

    <body>

    <div class="box">

    <h2>Teacher Login</h2>

    <form action="/login" method="post">

    <input type="text" name="username" placeholder="Username"><br>
    <input type="password" name="password" placeholder="Password"><br>

    <button type="submit">Login</button>

    </form>

    </div>

    </body>
    </html>
    """


# ---------------- LOGIN LOGIC ----------------
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    if username == "teacher" and password == "1234":
        return RedirectResponse(url="/teacher_dashboard", status_code=303)

    return HTMLResponse("<h3>Invalid Login</h3>")


# ---------------- DASHBOARD ----------------
@app.get("/teacher_dashboard", response_class=HTMLResponse)
async def teacher_dashboard():

    return """
    <html>
    <head>
    <title>Teacher Dashboard</title>

    <style>

    body{
        font-family:Arial;
        background:#eef2f3;
        text-align:center;
        padding-top:80px;
    }

    .box{
        background:white;
        padding:40px;
        width:500px;
        margin:auto;
        border-radius:10px;
        box-shadow:0px 0px 15px gray;
    }

    button{
        padding:10px 20px;
        background:#2196F3;
        color:white;
        border:none;
        cursor:pointer;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h2>Upload Class Image</h2>

    <form action="/upload" method="post" enctype="multipart/form-data">

    <input type="file" name="file"><br><br>

    <button type="submit">Run Face Recognition</button>

    </form>

    </div>

    </body>
    </html>
    """


# ---------------- UPLOAD + RESULT ----------------
@app.post("/upload", response_class=HTMLResponse)
async def upload_image(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = recognize_faces(file_path)

    # create table rows
    table_rows = ""
    for i, name in enumerate(results["recognized"], start=1):
        table_rows += f"<tr><td>{i}</td><td>{name}</td></tr>"

    html = f"""
    <html>

    <head>

    <title>Recognition Result</title>

    <style>

    body{{
        font-family:Arial;
        background:#f4f4f4;
        text-align:center;
        padding-top:40px;
    }}

    .stats{{
        background:white;
        padding:20px;
        width:500px;
        margin:auto;
        border-radius:10px;
        box-shadow:0px 0px 10px gray;
    }}

    table{{
        margin:auto;
        margin-top:30px;
        border-collapse:collapse;
        width:60%;
        background:white;
    }}

    th,td{{
        border:3px solid black;
        padding:12px;
        text-align:center;
        font-size:16px;
    }}

    th{{
        background:#ddd;
    }}

    img{{
        margin-top:30px;
        border-radius:10px;
        box-shadow:0px 0px 10px gray;
    }}

    </style>

    </head>

    <body>

    <div class="stats">

    <h2>Face Recognition Result</h2>

    <p><b>Total Faces:</b> {results['total_faces']}</p>
    <p><b>Recognized Students:</b> {results['recognized_count']}</p>
    <p><b>Unknown Faces:</b> {results['unknown_count']}</p>

    </div>

    <table>

    <tr>
        <th>Sr.no</th>
        <th>Recognized Names</th>
    </tr>

    {table_rows}

    </table>

    <br>

    <img src="/{results['output_image']}" width="900">

    <br><br>

    <a href="/teacher_dashboard">Upload Another Image</a>

    </body>

    </html>
    """

    return html