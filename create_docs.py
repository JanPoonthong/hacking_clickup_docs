#!/usr/bin/env python3

import argparse
import json
import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv(".env")

headers = {
    "Authorization": f"Bearer {os.environ.get('auth_token')}",
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


def put_text_to_docs(title, description, view_id, id):
    url = f"https://app.clickup.com/docs/v1/view/{view_id}/page/{id}?all_pages=false"
    payload = json.dumps(
        {
            "name": f"{title}",
            "content": json.dumps(
                {
                    "ops": [
                        {"insert": f"{description}"},
                        {
                            "insert": "\n",
                            "attributes": {
                                "block-id": "block-279da377-da16-4281-ab40-b75a9b1ae183"
                            },
                        },
                    ]
                }
            ),
        }
    )
    response = requests.put(url, data=payload, headers=headers)
    print(response.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This is a script for creating docs in ClickUp.com"
    )
    parser.add_argument("--title", type=str, help="Type your title of the docs")
    parser.add_argument(
        "--description", type=str, help="Type your description of the docs"
    )
    args = parser.parse_args()
    create_docs_clickup(args.title, args.description)
