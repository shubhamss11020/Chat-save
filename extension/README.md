# Chat-Save: Managed Browser Extension (Claude Team Connector)

A production-grade Chrome & Edge (Manifest V3) extension that automatically captures web chats on [Claude.ai](https://claude.ai) in real-time, delivering them directly to your organization's Chat-Save second brain.

---

## Key Features

1. **Automatic Real-Time Capture**:
   - Intercepts prompt submissions on Enter or Send click.
   - Monitors assistant streaming responses via DOM mutation tracking.
   - Finalizes conversation turns when Claude finishes generation or is stopped.
2. **Reliable Offline Outbox**:
   - Queues messages in `chrome.storage.local` if the server is offline or unreachable.
   - Automatic retry loop with exponential backoff and jitter.
   - Deduplicates identical message snapshots via content hash.
3. **On-Page Save Status HUD**:
   - Unobtrusive floating badge in Claude web UI showing current sync status:
     - `Chat-Save: Synced` (Green)
     - `Claude typing...` (Blue pulse)
     - `Saving...` (Indigo)
     - `Offline (N queued)` (Amber)
   - Clickable popover displaying active Conversation ID, last receipt, and a manual "Sync Now" trigger.
4. **Independent Fleet Monitoring & Telemetry**:
   - Sends periodic heartbeat to `/api/extension/heartbeat`.
   - Central dashboard tracks each employee's extension version, queue size, and last sync timestamp.
5. **Enterprise Deployment Ready**:
   - Supports Chrome Managed Storage (`storage.managed`) via `schema.json`.
   - IT administrators can pre-configure and lock `serverUrl`, `authToken`, and `userId` via Google Admin Console, Windows Registry (GPO), or Microsoft Intune.

---

## Installation & Developer Setup

### 1. Load Unpacked in Chrome or Edge
1. Open Chrome or Edge and navigate to `chrome://extensions` (or `edge://extensions`).
2. Enable **Developer mode** (toggle in top right corner).
3. Click **Load unpacked** and select the `extension/` folder in this repository.
4. The extension icon will appear in your browser toolbar.

### 2. Configure Settings
1. Click the Chat-Save toolbar icon and select **Settings & Logs**, or right-click the extension and choose **Options**.
2. Set:
   - **Chat-Save Server URL**: `http://localhost:8000` (or your central Render URL)
   - **Auth Token**: Your `MCP_AUTH_TOKEN` (or employee secret token)
   - **Employee Identifier**: Your username or email (e.g. `shubham` or `alex@company.com`)
3. Click **Test Connection** to verify server reachability.
4. Click **Save Settings**.

---

## Enterprise Policy Deployment (IT Administrators)

To automatically deploy and configure this extension for all employees without requiring manual configuration:

### Chrome / Edge Managed Policy Schema (`schema.json`)
The extension defines a managed storage schema:
- `serverUrl` (string): Central Chat-Save server endpoint.
- `authToken` (string): Pre-shared company token or per-user secret.
- `userId` (string): Employee email or machine username.
- `autoSync` (boolean): Default `true`.

### Windows Registry (GPO / Intune)
Add registry keys under:
`HKEY_LOCAL_MACHINE\Software\Policies\Google\Chrome\3rdparty\extensions\<EXTENSION_ID>\policy`
or
`HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Edge\3rdparty\extensions\<EXTENSION_ID>\policy`

Values:
- `serverUrl`: `"https://chat-save.onrender.com"`
- `authToken`: `"your-secure-mcp-token"`
- `userId`: `"${username}"` (or employee email mapped by Intune)
- `autoSync`: `1` (DWORD)
