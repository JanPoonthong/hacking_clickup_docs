import requests
import config

import sys

headers = {
    "Authorization": f"Bearer {config.auth_token}",
    "Content-Type": "application/json",
}


def create_docs_clickup(title, description):
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
    page = data["pages"][0]
    put_text_to_docs(title, description, page["view_id"], page["id"])


def title_and_description(title, description):
    return {f"""{{"name": "{title}"}}""", f"""{{"content": "{description}"}}"""}


def put_text_to_docs(title, description, view_id, id):
    url = f"https://app.clickup.com/docs/v1/view/{view_id}/page/{id}?all_pages=false"
    for i in title_and_description(f"{title}", f"{description}"):
        response = requests.put(url, data=i, headers=headers)
        print(response)


if __name__ == "__main__":
    # print(sys.argv)
    if (
        len(sys.argv) >= 3
        and "title:" in sys.argv
        and "description:" in sys.argv
    ):
        pass
        # create_docs_clickup(sys.argv[1], sys.argv[2])
    else:
        print(
            'Argument should be atleast 2, "python create_docs.py title: <the title> description: <the description>"'
        )
        sys.exit(1)

    title = []
    for k in sys.argv[2:]:
        if k == "description:":
            break
        title.append(k)
    print(title)
