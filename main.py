import os
import glob
import config
import sqlite3
import requests
import textwrap

from pathlib import Path


from reportlab.pdfgen import canvas

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


def create_docs_clickup():
    url = "https://app.clickup.com/v1/view"
    raw_data = """{
    "visibility": 1,
    "me_view": false,
    "id": "",
    "parent": {
        "id": 36742991,
        "type": 7
    },
    "grouping": {},
    "divide": {},
    "settings": {
        "show_task_locations": false,
        "show_timer": false,
        "show_subtasks": 1,
        "show_subtask_parent_names": false,
        "me_comments": true,
        "me_subtasks": true,
        "me_checklists": true,
        "show_closed_subtasks": false,
        "show_task_ids": false,
        "show_empty_statuses": false,
        "time_in_status_view": 1,
        "auto_wrap": false
    },
    "members": [],
    "group_members": [],
    "sorting": {
        "fields": []
    },
    "filters": {
        "show_closed": false,
        "search_custom_fields": false,
        "search_description": false,
        "fields": []
    },
    "columns": {
        "fields": [
            {
                "field": "assignee",
                "pinned": true,
                "hidden": false
            },
            {
                "field": "dueDate",
                "pinned": false,
                "hidden": false
            },
            {
                "field": "priority",
                "pinned": false,
                "hidden": false
            }
        ]
    },
    "permissions": {
        "edit_view": true,
        "delete_view": true,
        "can_unprotect": true,
        "comment": true
    },
    "auto_save": false,
    "board_settings": {},
    "name": "Doc",
    "type": 9,
    "standard_view": false,
    "create_page": true,
    "user_filter_settings": true
}"""
    response = requests.post(url, headers=headers, data=raw_data)
    data = response.json()["view"]
    put_text_to_docs(data["pages"][0]["view_id"], data["pages"][0]["id"])


def title_and_description(title, description):
    return {f"""{{"name": "{title}"}}""", f"""{{"content": "{description}"}}"""}


def put_text_to_docs(view_id, id):
    url = f"https://app.clickup.com/docs/v1/view/{view_id}/page/{id}?all_pages=false"
    for i in title_and_description("strager is my dad", "I don't have a mom"):
        response = requests.put(url, data=i, headers=headers)
        # print(response.json())


def main():
    # create_docs_clickup()
    create_folder()
    create_pdf()
    # save_zoho_drive()
    con.close()


main()
