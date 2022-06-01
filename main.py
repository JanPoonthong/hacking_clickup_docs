import glob
import os
import requests
import sqlite3
import textwrap
from pathlib import Path
from reportlab.pdfgen import canvas

import config

headers = {
    "Authorization": f"Bearer {config.auth_token}",
    "Content-Type": "application/json",
}

con = sqlite3.connect("document.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE docs (title text, description text)""")
except sqlite3.OperationalError:
    pass


def get_docs():
    try:
        response = requests.get(
            "https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&dir=desc&section=all",
            headers=headers,
        )
    except requests.exceptions.HTTPError:
        raise SystemExit("Bearer token expired")

    return response


def create_folder():
    for i in get_docs().json()["views"]:
        try:
            os.mkdir(f"{i['name']}")
            print("Created ", f"{i['name']}")
        except FileExistsError:
            print("Directory ", f"{i['name']}", " already exists")


def save_docs_db(title, description):
    cur.execute(
        "INSERT INTO docs VALUES (?, ?)".format(title.replace('"', '""')),
        (title, description),
    )
    con.commit()


def delete_db():
    cur.execute("DELETE FROM docs;")


def check_duplicate():
    cur.execute("SELECT * FROM docs")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def draw_wrapped_line(canvas, text, length, x_pos, y_pos, y_offset):
    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            canvas.drawString(x_pos, y_pos, wraps[x])
            y_pos -= y_offset
        y_pos += y_offset
    else:
        canvas.drawString(x_pos, y_pos, text)
    return y_pos


def create_pdf():
    delete_db()
    for i in get_docs().json()["views"]:
        os.chdir(i["name"])
        for j in i["pages"]:
            save_docs_db(j["name"], j["text_content"])
            my_canvas = canvas.Canvas(f"{j['name']}.pdf")
            my_canvas.setFont("Helvetica", 20)
            my_canvas.drawString(100, 750, f"{j['name']}")
            my_canvas.setFont("Helvetica", 12)
            draw_wrapped_line(
                my_canvas, f"{j['text_content']}", 80, 100, 730, 15
            )
            my_canvas.save()
        os.chdir("../")
    print("Update PDF")


def zoho_token():
    url = "https://accounts.zoho.com/oauth/v2/token?refresh_token={config.zoho_refresh_token}&client_secret={config.zoho_client_secret}&grant_type=refresh_token&client_id={config.zoho_client_id}"
    access_token = requests.post(url)
    return access_token["access_token"]


def save_zoho_drive():
    url = "https://www.zohoapis.com/workdrive/api/v1/upload?parent_id=hltaja4afd79bedb04e93bcede5e7e897802f&override-name-exist=true"
    for path in Path("./").rglob("*.pdf"):
        files = {"content": open(f"{path}", "rb")}
        headers = {"Authorization": f"Zoho-oauthtoken {config.file_zoho_token}"}
        response = requests.post(url, files=files, headers=headers)
        # print(response.json())


def main():
    # create_docs_clickup()
    create_folder()
    create_pdf()
    # save_zoho_drive()
    con.close()


main()
