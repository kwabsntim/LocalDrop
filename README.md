# LocalDrop

A lightweight local network file transfer tool for sending files and links between your phone and computer over the same Wi-Fi network. No internet connection required.

## Features

- Two-way file transfer — send files from phone to desktop and desktop to phone
- Two-way link sharing — share URLs in both directions
- Real-time updates on both sides using HTMX polling (no manual refresh needed)
- Toast notifications on send — no page navigation, stays where you are
- Connection status indicator — green dot + "Active" in the navbar when a phone is connected
- Phone auto-receives new files and links from the desktop without refreshing
- Separated received sections — desktop shows files from phone, phone shows files from desktop
- QR code based connection — scan once and you're connected
- Local IP address auto-detection
- Dark theme UI on both desktop and mobile
- Development and production configurations

## How it works

1. Run the server on your computer
2. Open `http://localhost:5000` in your desktop browser
3. A QR code is shown pointing to your computer's local IP address
4. Scan the QR code with your phone (both devices must be on the same Wi-Fi network)
5. The navbar shows a green **Active** dot when the phone is connected
6. Send files and links in either direction — a toast notification confirms each send
7. Files and links appear on the receiving side automatically within a few seconds

## Project Structure

```
LocalDrop/
    app.py                      # Main Flask application with all routes
    config.py                   # Development and production configurations
    requirements.txt            # Python dependencies
    uploads/                    # Directory where uploaded files are stored (auto-created)
    static/
        style.css               # Dark theme styling for the desktop UI
    templates/
        index.html              # Desktop home page — QR code, send forms, received section
        connect.html            # Phone page — send forms, received files and links
        status_content.html     # HTMX partial — desktop received files and links
        phone_updates.html      # HTMX partial — phone received files and links
        status.html             # Full status page (legacy reference)
        updates.html            # Legacy updates partial
```

## Requirements

- Python 3.8 or higher
- Flask
- qrcode
- Pillow
- werkzeug

## Installation

```bash
git clone https://github.com/kwabsntim/LocalDrop.git
cd LocalDrop
pip install -r requirements.txt
```

## Running the App

### Development Mode (Port 5000)
```bash
python app.py
```

### Production Mode (Port 3030)
```bash
FLASK_ENV=production python app.py
```

The server auto-detects your local IP and generates a QR code. Open `http://localhost:5000` in your browser (or use your machine's local IP from another device on the same network).

## Configuration

Managed in `config.py`:

| Mode | Debug | Port |
|------|-------|------|
| Development | On | 5000 |
| Production | Off | 3030 |

Set `FLASK_ENV=production` to switch to production mode.

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Desktop home page |
| `/connect` | GET | Phone connection page (scanned from QR code) |
| `/status` | GET | HTMX polling endpoint — desktop received files and links |
| `/nav_status` | GET | HTMX polling endpoint — navbar connection badge |
| `/phone_updates` | GET | HTMX polling endpoint — phone received files and links |
| `/upload` | POST | Upload a file (from phone or desktop) |
| `/send_link` | POST | Send a link (from phone or desktop) |
| `/uploads/<filename>` | GET | Download a previously uploaded file |

## File Transfer Flow

### Desktop → Phone
1. Connect your phone by scanning the QR code
2. Use the **Send File** or **Send Link** forms on the desktop
3. A toast notification confirms the send without leaving the page
4. The file or link appears on the phone's received section within 3 seconds (no refresh needed)

### Phone → Desktop
1. Use the **Send File** or **Send Link** forms on the phone's connected page
2. A toast notification confirms the send
3. The file or link appears in the desktop's received section within 2 seconds (no refresh needed)

## Connection Timeout

If the phone does not make a request for 5 minutes, the connection is considered dropped and the desktop returns to showing the QR code.

## Allowed File Types

`txt`, `pdf`, `png`, `jpg`, `jpeg`, `gif`, `docx`, `pptx`, `xlsx`, `csv`, `zip`, `rar`

## Notes

- Both devices must be on the same local Wi-Fi network
- Files are stored in the `uploads/` directory on the computer running the server
- File and link history resets when the server is restarted (in-memory storage)
- The app is intended for personal local use — there is no authentication

## Browser Support

Chrome, Firefox, Safari, Edge — desktop and mobile.

## Features to be Shipped

- **Copy-to-clipboard on received links** — a copy button next to each link instead of just a plain anchor
- **File deletion** — remove individual files from the received section and from disk
- **Duplicate filename handling** — prevent silent overwrites by appending a counter on conflict e.g. `photo_1.jpg`
- **Persist data across restarts** — use SQLite to store filenames and links so history survives server restarts
- **File size and timestamp on file cards** — show metadata under each file in the received section
- **Upload progress indicator** — progress bar feedback while large files are uploading
- **Download all as ZIP** — one button to bundle everything received into a single zip download
- **PIN protection for /connect** — passphrase check on the phone page so only the QR scanner can access it
- **Rate limiting on uploads** — cap upload requests per IP to prevent disk flooding
- **Multi-device support** — session model allowing multiple phones to connect with isolated send/receive queues
- **Browser notifications on desktop** — Web Notifications API alert when a file or link arrives from the phone
- **Auto-clear old files** — automatically delete files from `uploads/` after a configurable number of days
