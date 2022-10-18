# Common

Shared endpoints

**URL** : `/api/v1/common/ipblacklist`

**Methods** : `GET`

**Auth required** : YES

**Data constraints**

```json
{
  "token": "<VALID API TOKEN>"
}
```

**Data example**

```json
{
  "token": "123bhg34hv5h4v"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "ips": [<List of addresses blacklisted>]
}
```

## Error Response

**Condition** : If 'token' is wrong

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "non_field_errors": ["Incorrect API TOKEN"]
}
```

---

**URL** : `/api/v1/common/ipblacklist`

**Methods** : `POST`

**Auth required** : YES

**Data constraints**

```json
{
  "token": "<VALID API TOKEN>",
  "ips": [<List of addresses to blacklist>]
}
```

**Data example**

```json
{
  "token": "123bhg34hv5h4v",
  "ips": ["192.168.0.69", "192.168.0.137", "192.168.0.8"]
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "ips": [<List of addresses blacklisted>]
}
```

## Error Response

**Condition** : If 'token' is wrong

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "non_field_errors": ["Incorrect API TOKEN"]
}
```

**URL** : `/api/v1/common/ipblacklist`

**Methods** : `GET`

**Auth required** : YES

**Data constraints**

```json
{
  "token": "<VALID API TOKEN>"
}
```

**Data example**

```json
{
  "token": "123bhg34hv5h4v"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "ips": [<List of addresses blacklisted>]
}
```

## Error Response

**Condition** : If 'token' is wrong

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "non_field_errors": ["Incorrect API TOKEN"]
}
```

---

**URL** : `/api/v1/common/ipwhitelist`

**Methods** : `POST`

**Auth required** : YES

**Data constraints**

```json
{
  "token": "<VALID API TOKEN>",
  "ips": [<List of addresses to whitelist>]
}
```

**Data example**

```json
{
  "token": "123bhg34hv5h4v",
  "ips": ["192.168.0.69", "192.168.0.137", "192.168.0.8"]
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "ips": [<List of addresses whitelisted>]
}
```

## Error Response

**Condition** : If 'token' is wrong

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "non_field_errors": ["Incorrect API TOKEN"]
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
