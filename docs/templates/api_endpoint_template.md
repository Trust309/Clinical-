# API Endpoint Template

Use this template when documenting a new API endpoint.

---

## Endpoint Name: `[METHOD] /endpoint-path`

### Description
[Brief description of what this endpoint does]

### HTTP Method
`[GET/POST/PUT/DELETE]`

### URL
```
/endpoint-path
```

### Authentication
- [ ] Required
- [ ] Optional
- [ ] Not required

[If required, describe authentication method]

### Request Parameters

#### Headers
| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Content-Type | string | Yes | Must be `application/json` |
| [header-name] | [type] | [Yes/No] | [description] |

#### Body Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| [param1] | [string/number/boolean/object] | [Yes/No] | [description] | `"example"` |
| [param2] | [type] | [Yes/No] | [description] | `123` |

#### Query Parameters
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| [param1] | [type] | [Yes/No] | [description] | [default value] |

### Request Example

```bash
curl -X [METHOD] http://localhost:5000/endpoint-path \
  -H "Content-Type: application/json" \
  -d '{
    "param1": "value1",
    "param2": "value2"
  }'
```

```javascript
// JavaScript example
fetch('http://localhost:5000/endpoint-path', {
  method: '[METHOD]',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    param1: 'value1',
    param2: 'value2'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Response

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "field1": "value1",
    "field2": "value2"
  },
  "message": "Operation successful"
}
```

#### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Indicates if operation was successful |
| data | object | Response payload |
| message | string | Human-readable message |

#### Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "error": "Invalid parameter: [param_name]",
  "message": "Detailed error message"
}
```

**404 Not Found**
```json
{
  "success": false,
  "error": "Resource not found",
  "message": "The requested resource does not exist"
}
```

**500 Internal Server Error**
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

### Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected error occurred |

### Notes

- [Any special considerations, limitations, or gotchas]
- [Performance considerations]
- [Rate limiting information]
- [Deprecation warnings if applicable]

### Examples & Use Cases

#### Use Case 1: [Common use case name]
[Description of the use case]

```bash
# Example command
```

**Expected Result:**
```json
{
  // Expected response
}
```

#### Use Case 2: [Another use case]
[Description]

### Related Endpoints

- [`[METHOD] /related-endpoint`](#) - [Brief description]
- [`[METHOD] /another-endpoint`](#) - [Brief description]

### Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |

---

**Last Updated**: [Date]  
**Maintained By**: [Your Name/Team]
