# API Documentation

This document describes all available API endpoints for the Clinical Supervision Chatbot.

## Base URL

```
http://localhost:5000
```

## Endpoints

### `GET /`

 Serve the chatbot interface 

**Example Request:**

```bash
curl -X GET http://localhost:5000/
```

---

### `POST /chat`

 Handle chat messages 

**Example Request:**

```bash
curl -X POST http://localhost:5000/chat
```

---

### `GET /history`

 Get conversation history 

**Example Request:**

```bash
curl -X GET http://localhost:5000/history
```

---

### `POST /reset`

 Reset conversation history 

**Example Request:**

```bash
curl -X POST http://localhost:5000/reset
```

---

