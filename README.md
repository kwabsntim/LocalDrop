# LocalDrop

A lightweight local network file transfer tool that lets you send files and links between your phone and computer over the same Wi-Fi network. No internet connection required.

## Features

- Send files from phone to desktop and vice versa
- Share links between devices
- Real-time file updates using HTMX polling
- Responsive UI for both desktop and mobile
- Dark theme interface
- QR code based connection
- Local IP address detection
- Development and production configurations

## How it works

1. Run the server on your computer
2. A QR code is generated on the home page pointing to your computer's local IP address
3. Scan the QR code with your phone to connect
4. Send files and links directly between your devices over the local network
5. Desktop shows recent files in a permanent sidebar
6. Phone displays connected status with upload/link forms

## Project Structure

```
LocalDrop/
    app.py                  # Main Flask application with all routes
    config.py               # Development and production configurations
    requirements.txt        # Python dependencies
    uploads/                # Directory where uploaded files are stored
    static/
        style.css           # Dark theme styling for desktop UI
    templates/
        index.html          # Desktop home page with QR code and sidebar
        connect.html        # Phone connection page with forms
        status_content.html # Content swap template for HTMX polling
        status.html         # Full status page (for reference)
```

## Requirements

- Python 3.8 or higher
- Flask
- qrcode
- Pillow
- werkzeug

## Installation

Clone the repository and install the dependencies:

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

The server automatically detects your local IP and generates a QR code. Open your browser and go to `http://localhost:5000` (or your machine's local IP address).

## Configuration

Configurations are managed in `config.py`:

- **Development**: Debug mode enabled, runs on port 5000
- **Production**: Debug mode disabled, runs on port 3030

Set the environment variable `FLASK_ENV` to switch between modes.

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Desktop home page with QR code |
| `/connect` | GET | Phone connection page |
| `/status` | GET | Connection status endpoint (HTMX) |
| `/upload` | POST | Upload file from phone/desktop |
| `/send_link` | POST | Send link between devices |
| `/uploads/<filename>` | GET | Download uploaded file |

## File Transfer Flow

1. **Desktop → Phone**: Use the desktop forms to upload files or send links
2. **Phone → Desktop**: Use the phone forms to upload files or send links
3. **Real-time Updates**: Files appear in the sidebar automatically via HTMX polling
4. **Download**: Click on any file to download it

## Browser Support

- Chrome/Chromium
- Firefox
- Safari
- Edge

Works on both desktop and mobile browsers.
````

```
http://localhost:5000
```

Scan the QR code shown on the page with your phone (make sure both devices are on the same Wi-Fi network).

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page, displays the QR code |
| `/connect` | Phone hits this route when it scans the QR code |
| `/status` | Shows whether a phone is currently connected |

## Notes

- Both devices must be on the same local Wi-Fi network.
- The server auto-detects the local IP address of the computer.
- Files are stored in the `uploads/` directory on the computer.
