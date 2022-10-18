# Common

Shared endpoints

**URL** : `/api/v1/common/ipblacklist`

**Method** : `GET`

**Auth required** : YES

**Data constraints**

```json
{
  "username": "[valid email address]",
  "password": "[password in plain text]"
}
```

**Data example**

```json
{
  "username": "iloveauth@example.com",
  "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "non_field_errors": ["Unable to login with provided credentials."]
}
```

# wingoEDR

Endpoints in relation to wingoEDR

**URL** : `/api/v1/wingoEDR/updateconfig`

**Method** : `GET`

**Auth required** : YES

**Data constraints**

```json
{
  "username": "[valid email address]",
  "password": "[password in plain text]"
}
```

**Data example**

```json
{
  "username": "iloveauth@example.com",
  "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`
