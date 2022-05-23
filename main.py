import os
import config
import sqlite3
import requests

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

    response = requests.get(
        "https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&dir=desc&section=all",
        headers=headers,
    )
    return response


def create_folder():
    for i in get_docs().json()["views"]:
        try:
            os.mkdir(f"{i['name']}")
        except FileExistsError:
            print("Directory ", f"{i['name']}", " already exists")


def save_docs_db(title, description):
    cur.execute(
        "INSERT INTO docs VALUES (?, ?)".format(title.replace('"', '""')),
        (title, description),
    )
    con.commit()


def create_pdf():
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
    print("Create PDF")
    con.close()


def main():
    create_folder()
    create_pdf()


main()
