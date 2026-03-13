# LocalDrop

A lightweight local network file transfer tool that lets you send files between your phone and computer over the same Wi-Fi network. No internet connection required.

## How it works

1. Run the server on your computer.
2. A QR code is generated on the home page pointing to your computer's local IP address.
3. Scan the QR code with your phone to connect.
4. Transfer files directly between your devices over the local network.

## Project Structure

```
LocalDrop/
    app.py              # Main Flask application
    requirements.txt    # Python dependencies
    uploads/            # Directory where uploaded files are stored
    static/             # Static assets (CSS, JS, images)
    templates/
        index.html      # Home page with QR code
        connect.html    # Phone connection landing page
        status.html     # Connection status page
        updates.html    # Transfer updates page
```

## Requirements

- Python 3.8 or higher
- Flask
- qrcode
- Pillow

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/kwabsntim/LocalDrop.git
cd LocalDrop
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

The server starts on port `5000` and is accessible on all network interfaces. Open your browser and go to:

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
