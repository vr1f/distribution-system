# REST API endpoint for aid recipients

- Endpoint path: `/aid_recipient`
- Accepted methods: `POST | PUT | DELETE`

## `POST | PUT`: Create (or update) a recipient

Creates a new recipient in the system. The `PUT` method additionally permits overriding an existing entry and should be used for updating recipient information.

### Request

A `json` object representing an `AidRecipient` (refer to [recipients.py][recipients_py]).

Minimum required fields:
```json
{
  "first_name": "foo",
  "age": 25,
}
```

Expanded fields:
```json
{
  "first_name": "foo",
  "age": 25,
  "address": "statue of liberty",
  "common_law_partner": {
    "first_name": "bar",
    "age": 25
  },
  "dependents": [
    {
      "first_name": "power",
      "last_name": "ranger",
      "age": 8
    },
    {
      "first_name": "mickey",
      "last_name": "mouse",
      "age": 8
    }
  ]
}
```

### Response

A `json` object representing an `DatabaseActionResponse` (refer to [recipients.py][responses_py]).

```json
{
  "id": "1234abcd",
  "error": null
}
```

## `DELETE`: Create a recipient

Creates a new recipient in the system. The `PUT` method additionally permits overriding an existing entry and should be used for updating recipient information.

### Request

A `json` object representing an `PersonID` (refer to [recipients.py][recipients_py]).

```json
{
  "id": "1234abcd"
}
```

### Response

A `json` object representing an `DatabaseActionResponse` (refer to [recipients.py][responses_py]).

```json
{
  "id": "1234abcd",
  "error": null
}
```




[recipients_py]: ../../src/recipients.py
[responses_py]: ../../src/responses.py