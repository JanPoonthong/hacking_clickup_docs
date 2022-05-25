import os
import glob
import config
import sqlite3
import requests
from pathlib import Path


from reportlab.pdfgen import canvas

con = sqlite3.connect("document.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE docs (title text, description text)""")
except sqlite3.OperationalError:
    pass


def get_docs():
    headers = {
        "Authorization": f"Bearer {config.auth_token}",
        "Content-Type": "application/json",
    }

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


def create_pdf():
    delete_db()
    for i in get_docs().json()["views"]:
        os.chdir(i["name"])
        for j in i["pages"]:
            save_docs_db(j["name"], j["text_content"])
            my_canvas = canvas.Canvas(f"{j['name']}.pdf")
            my_canvas.setFont("Helvetica", 20)
            my_canvas.drawString(100, 750, f"Title: {j['name']}")
            my_canvas.setFont("Helvetica", 12)
            my_canvas.drawString(100, 730, f"Description: {j['text_content']}")
            my_canvas.save()
        os.chdir("../")
    print("Update PDF")


def save_zoho_drive():
    for path in Path("./").rglob("*.pdf"):
        files = {"upload_file": open(f"{path.name}", "rb")}
        headers = {"Authorization": f"Zoho-oauthtoken {config.file_zoho_token}"}
        requests.post(
            "https://www.zohoapis.com/workdrive/api/v1/upload?parent_id=hltaja4afd79bedb04e93bcede5e7e897802f",
            files=files,
            headers=headers,
        )


def main():
    # create_folder()
    # create_pdf()
    save_zoho_drive()
    # con.close()


main()
