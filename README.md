# Hacking ClickUp Docs

## API for login in and can also get bearer authorization key

**API -> https://app.clickup.com/v1/login?include_teams=true**

1. Go https://www.base64decode.org/, and click the encode option to encode your email and password. For example, `username@gmail.com:password`.

2. When you get the encoded email and password, i.e `dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk`. Add `Basic` in front of the token. For example, `Basic dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk`.

3. `POST` Request to API with a basic token above. `{Authorization: Basic dXNlcm5hbWVAZ21haWwuY29tOnBhc3N3b3Jk}` as a header.

4. After step 3, you can get the `token` which is `Bearer ejasdhjasjkdyasjkdhjbasdas.asjlkdhasjkdhjkasdhjkasndjaskas`.

## API for getting all docs

**API -> https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&order_by=date_viewed&dir=desc&section=all**

1. When requesting this API, make sure you add `{Authorization: Bearer ejasdhjasjkdyasjkdhjbasdas.asjlkdhasjkdhjkasdhjkasndjaskas}` as a header.

Get access token: https://app.clickup.com/api/v2/oauth/token?client_id={}&client_secret={}&code={}

Get team id: https://api.clickup.com/api/v2/team

Get user id: https://api.clickup.com/api/v2/user
