# Hacking ClickUp Docs

## Requirements

### Linux / macOS / Windows

Prerequisites:

- [Python][python-download]

Instructions:

1.  Download requests:

        $ pip install requests

## Create doc in ClickUp

Instructions:

1.  Run:

        $ python3 create_docs.py --title "Your Title" --description "Your Description"


## API for login in and can also get bearer authorization key

**API -> https://app.clickup.com/v1/login?include_teams=true**

1. Go https://www.base64decode.org/, and click the encode option to encode your email and password(ClickUp email and password). For example, `username@gmail.com:password`.

2. When you get the encoded email and password, i.e `dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk`. Add `Basic` in front of the token. For example, `Basic dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk`.

3. `POST` Request to API with a basic token above. `{Authorization: Basic dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk}` as a header.

4. After step 3, you will get a json. Inside the json object you find `token` which is `Bearer ejasdhjasjkdyasjkdhjbasdas.asjlkdhasjkdhjkasdhjkasndjaskas`.

## API for getting all docs

**API -> https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&order_by=date_viewed&dir=desc&section=all**

1. When requesting this API, make sure you add `{Authorization: Bearer ejasdhjasjkdyasjkdhjbasdas.asjlkdhasjkdhjkasdhjkasndjaskas}` as a header.

## Get access token:

**API -> https://app.clickup.com/api/v2/oauth/token?client_id={}&client_secret={}&code={}**

1. [Click to open docs][access_token]

## Get team id

**API -> https://api.clickup.com/api/v2/team**

## Get user id

**API -> https://api.clickup.com/api/v2/user**

[access_token]: https://jsapi.apiary.io/apis/clickup20/introduction/authentication/oauth2-flow.html
[python-download]: https://www.python.org/downloads/
