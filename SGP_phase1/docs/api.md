# API Documentation

## REST API Endpoints

### Base URL
```
http://<local-ip>:5000/api
```

## File Operations

### Upload File

<div class="api-card">

**Endpoint:** `POST /upload`

**Description:** Upload a file to the server

**Request:**
```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | The file to upload |

**Example Request:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Success Response (200):**
```json
{
    "success": true,
    "filename": "example.pdf",
    "size": 1048576,
    "upload_time": "2024-03-15T10:30:00Z"
}
```

**Error Response (400):**
```json
{
    "error": "No file provided",
    "code": "MISSING_FILE"
}
```

</div>

### Download File

<div class="api-card">

**Endpoint:** `GET /download/<filename>`

**Description:** Download a previously uploaded file

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filename | String | Yes | Name of the file to download |

**Example Request:**
```javascript
fetch('/download/example.pdf')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'example.pdf';
        a.click();
    });
```

**Success Response (200):**
- Returns file binary data with appropriate Content-Type header

**Error Response (404):**
```json
{
    "error": "File not found",
    "code": "FILE_NOT_FOUND"
}
```

</div>

### List Files

<div class="api-card">

**Endpoint:** `GET /files`

**Description:** Get list of all available files

**Example Request:**
```javascript
fetch('/files')
    .then(response => response.json())
    .then(data => console.log(data));
```

**Success Response (200):**
```json
{
    "files": [
        {
            "name": "document.pdf",
            "size": 1048576,
            "modified": "2024-03-15T10:30:00Z",
            "type": "application/pdf"
        },
        {
            "name": "image.jpg",
            "size": 524288,
            "modified": "2024-03-15T09:15:00Z",
            "type": "image/jpeg"
        }
    ],
    "total": 2
}
```

</div>

### Delete File

<div class="api-card">

**Endpoint:** `DELETE /files/<filename>`

**Description:** Delete a file from the server

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filename | String | Yes | Name of the file to delete |

**Example Request:**
```javascript
fetch('/files/example.pdf', {
    method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "File deleted successfully"
}
```

</div>

## Authentication API (Phase 3)

### Generate Token

<div class="api-card planned">

**Endpoint:** `POST /auth/token`

**Description:** Generate an authentication token

**Request Body:**
```json
{
    "username": "user@example.com",
    "password": "secure_password"
}
```

**Success Response (200):**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400,
    "token_type": "Bearer"
}
```

**Error Response (401):**
```json
{
    "error": "Invalid credentials",
    "code": "INVALID_CREDENTIALS"
}
```

</div>

### Validate Token

<div class="api-card planned">

**Endpoint:** `GET /auth/validate`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
    "valid": true,
    "user_id": 123,
    "expires_at": "2024-03-16T10:30:00Z"
}
```

</div>

### Revoke Token

<div class="api-card planned">

**Endpoint:** `DELETE /auth/token`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Token revoked successfully"
}
```

</div>

## API Flow Diagram

<div class="mermaid-container">

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant Storage
    
    Note over Client,Storage: File Upload Flow
    
    Client->>API: POST /upload
    API->>Auth: Validate Token (Phase 3)
    
    alt Token Valid
        Auth-->>API: Authorized
        API->>Storage: Save File
        Storage-->>API: File Saved
        API-->>Client: 200 Success
    else Token Invalid
        Auth-->>API: Unauthorized
        API-->>Client: 401 Error
    end
    
    Note over Client,Storage: File Download Flow
    
    Client->>API: GET /download/:filename
    API->>Auth: Validate Token
    Auth-->>API: Authorized
    API->>Storage: Retrieve File
    Storage-->>API: File Data
    API-->>Client: 200 + File Stream
    
    Note over Client,Storage: File List Flow
    
    Client->>API: GET /files
    API->>Auth: Validate Token
    Auth-->>API: Authorized
    API->>Storage: List Files
    Storage-->>API: File Metadata
    API-->>Client: 200 + JSON
</mermaid>

</div>

## Error Codes Reference

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| MISSING_FILE | 400 | No file in request | Include file in FormData |
| FILE_TOO_LARGE | 413 | File exceeds size limit | Reduce file size |
| INVALID_FILE_TYPE | 415 | File type not allowed | Check allowed types |
| FILE_NOT_FOUND | 404 | File doesn't exist | Verify filename |
| STORAGE_FULL | 507 | Server storage full | Free up space |
| INVALID_CREDENTIALS | 401 | Wrong username/password | Check credentials |
| TOKEN_EXPIRED | 401 | Auth token expired | Request new token |
| INSUFFICIENT_PERMISSIONS | 403 | No access permission | Contact admin |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait and retry |
| INTERNAL_ERROR | 500 | Server error | Report to admin |

## Rate Limiting (Phase 3)

<div class="mermaid-container">

```mermaid
graph LR
    A[API Request] --> B{Check Rate Limit}
    
    B -->|Under Limit| C[Process Request]
    B -->|Over Limit| D[Return 429 Error]
    
    C --> E[Update Counter]
    E --> F[Return Response]
    
    D --> G[Include Retry-After Header]
    
    style A fill:#3b82f6
    style C fill:#10b981
    style D fill:#ef4444
</mermaid>

</div>

**Rate Limits (Planned):**
- Upload: 10 files per minute
- Download: 50 files per minute
- List Files: 30 requests per minute
- Authentication: 5 attempts per minute

**Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1647345600
```

## WebSocket API (Phase 3)

### Real-Time File Updates

<div class="api-card planned">

**Endpoint:** `ws://<local-ip>:5000/ws`

**Events:**

#### `file.uploaded`
```json
{
    "event": "file.uploaded",
    "data": {
        "filename": "newfile.pdf",
        "size": 1048576,
        "uploader": "user@example.com",
        "timestamp": "2024-03-15T10:30:00Z"
    }
}
```

#### `file.deleted`
```json
{
    "event": "file.deleted",
    "data": {
        "filename": "oldfile.pdf",
        "timestamp": "2024-03-15T10:35:00Z"
    }
}
```

#### `upload.progress`
```json
{
    "event": "upload.progress",
    "data": {
        "filename": "largefile.zip",
        "progress": 45,
        "bytes_transferred": 472907776,
        "total_bytes": 1048576000
    }
}
```

**Example Client:**
```javascript
const ws = new WebSocket('ws://192.168.1.100:5000/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Event:', data.event, 'Data:', data.data);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
```

</div>

## SDK Examples

### Python SDK

```python
import requests

class ShareJadPiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def upload_file(self, filepath):
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f'{self.base_url}/upload',
                files=files
            )
            return response.json()
    
    def list_files(self):
        response = self.session.get(f'{self.base_url}/files')
        return response.json()
    
    def download_file(self, filename, save_path):
        response = self.session.get(
            f'{self.base_url}/download/{filename}',
            stream=True
        )
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

# Usage
client = ShareJadPiClient('http://192.168.1.100:5000')
result = client.upload_file('document.pdf')
print(f"Uploaded: {result['filename']}")
```

### JavaScript SDK

```javascript
class ShareJadPiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.baseUrl}/upload`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
    
    async listFiles() {
        const response = await fetch(`${this.baseUrl}/files`);
        return await response.json();
    }
    
    async downloadFile(filename) {
        const response = await fetch(
            `${this.baseUrl}/download/${filename}`
        );
        const blob = await response.blob();
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}

// Usage
const client = new ShareJadPiClient('http://192.168.1.100:5000');
await client.uploadFile(fileInput.files[0]);
const files = await client.listFiles();
```

## API Testing

### cURL Examples

**Upload File:**
```bash
curl -X POST http://192.168.1.100:5000/upload \
  -F "file=@/path/to/file.pdf"
```

**List Files:**
```bash
curl http://192.168.1.100:5000/files
```

**Download File:**
```bash
curl http://192.168.1.100:5000/download/file.pdf \
  -o downloaded_file.pdf
```

**Delete File:**
```bash
curl -X DELETE http://192.168.1.100:5000/files/file.pdf
```

### Postman Collection

Import this collection for testing:

```json
{
  "info": {
    "name": "ShareJadPi API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/"
  },
  "item": [
    {
      "name": "Upload File",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/upload",
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "src": []
            }
          ]
        }
      }
    },
    {
      "name": "List Files",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/files"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://192.168.1.100:5000"
    }
  ]
}
```

<style>
.api-card {
  background: var(--vp-c-bg-soft);
  border-left: 4px solid var(--vp-c-brand);
  padding: 20px;
  margin: 20px 0;
  border-radius: 8px;
}

.api-card.planned {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, var(--vp-c-bg-soft) 0%, rgba(245, 158, 11, 0.05) 100%);
}

.api-card h4 {
  margin-top: 0;
}

.mermaid-container {
  position: relative;
  margin: 2rem 0;
  padding: 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  border: 1px solid var(--vp-c-divider);
  overflow: hidden;
}

code {
  background: var(--vp-c-bg-mute);
  padding: 2px 6px;
  border-radius: 4px;
}
</style>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const containers = document.querySelectorAll('.mermaid-container')
  
  containers.forEach(container => {
    const controls = document.createElement('div')
    controls.className = 'diagram-controls'
    controls.innerHTML = `
      <button class="zoom-in">🔍+</button>
      <button class="zoom-out">🔍-</button>
      <button class="reset-zoom">↺</button>
      <button class="fullscreen">⛶</button>
    `
    container.style.position = 'relative'
    container.insertBefore(controls, container.firstChild)
  })
})
</script>
