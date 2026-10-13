---
conversation_id: 9d0fbea5-ea1c-4ed8-880b-95ce4553a46d
platform: claude
username: "harsh"
title: "Odoo JSON RPC connection requirements - Claude"
created_at: "2026-10-13 13:17:39 EDT"
updated_at: "2026-10-13 14:51:03 EDT"
---

# Odoo JSON RPC connection requirements - Claude

## User (2026-10-13 13:17:30 EDT)

do we need db name to connect to odoo platform through Json RPC or will server url, password and id would do?

## Claude (2026-10-13 13:17:39 EDT)

> *Thinking:*
>

To connect to Odoo via JSON-RPC, you'll need **the database name** in addition to the server URL, password, and ID. Here's why:

## Required Parameters for Odoo JSON-RPC

1. **Server URL** ✓ (you have this)
2. **Database Name** ✗ (required - you need this)
3. **Username or User ID** ✓ (you have this)
4. **Password** ✓ (you have this)

## Why Database Name Matters

- An Odoo server can host **multiple databases** at the same URL
- The API needs to know which database to query
- The database name is required in almost all JSON-RPC method calls (e.g., `web.session.authenticate`, `object.execute`, etc.)

## Typical Authentication Flow

```javascript
// 1. Authenticate (requires database name)
POST /jsonrpc
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "common",
    "method": "authenticate",
    "args": [database_name, username, password]
  }
}

// 2. Subsequent calls (also requires database name)
POST /jsonrpc
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute",
    "args": [database_name, uid, password, model, method, ...]
  }
}
```

## The Exception

Some Odoo instances are configured as **single-database setups** with a custom REST API layer that might abstract away the database name requirement—but this would be non-standard customization.

**Bottom line:** Get the database name from your Odoo administrator. It's typically visible in the login page URL or Odoo settings.
