from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import io
from typing import Optional
import logging
import pathlib
import sys

start = '<li> <input type="checkbox" id="%d"> <label for="%d">%s</label> </li>\n'
section = '<b>%s</b>\n'
ERR_INVALID_FILE = 1
INPUT_FILE = pathlib.Path('./questions.txt')

def replace() -> str:
    out = io.StringIO()

    if not INPUT_FILE.exists() or not INPUT_FILE.is_file():
        print("Invalid input File", file=sys.stderr)
        exit(ERR_INVALID_FILE)


    with open(INPUT_FILE) as f_in:
        i = 1
        for line in f_in:
            if i == 101:
                break
            if not line:
                continue
            line = line.strip()
            if line.endswith(":"):
                out.write(section % line)
            else:
                out.write(start % (i, i, line))
                i += 1
    return out.getvalue()

with open("./index.html") as f:
    root_page = f.read().replace("{{ questions }}", replace())

# Logger
score_metrics = logging.getLogger("scores")
score_metrics.setLevel(logging.DEBUG)
sm_fh = logging.FileHandler("logs/score.log", encoding="utf-8")
sm_fm = logging.Formatter('%(asctime)s %(message)s')
sm_fh.setFormatter(sm_fm)
score_metrics.addHandler(sm_fh)

error_metrics = logging.getLogger("parse_exceptions")
error_metrics.setLevel(logging.DEBUG)
em_fh = logging.FileHandler("logs/errors.log", encoding="utf-8")
em_fm = logging.Formatter('%(asctime)s %(message)s')
em_fh.setFormatter(em_fm)
error_metrics.addHandler(em_fh)

app = FastAPI()

def list_to_string(l: list) -> Optional[str]:
    """We assume the length of the list is 100"""
    for element in l:
        if element != 0 or element != 1:
            return None
    out = io.StringIO()
    out.write("[")
    out.write(str(l[0]))
    for i, val in enumerate(l):
        if i == 0:
            continue
        out.write(f",{str(val)}")
    out.write("]")    
    return out.getvalue()


@app.get("/", response_class=HTMLResponse)
def root():
    return root_page


@app.post("/submit", status_code=201)
async def submit(request: Request):
    try:
        json_data = await request.json()
        if not isinstance(json_data, list):
            return None
        if len(json_data) != 100:
            return None
        stringified_json = list_to_string(json_data)
        if stringified_json is None:
            return None
        if request.client:
            ip = request.client.host
            score_metrics.info(f"{ip} {stringified_json}")
    except Exception as e:
        error_metrics.info(e)
    # Save the IP Address, timestamp, overall score, and individual scores
