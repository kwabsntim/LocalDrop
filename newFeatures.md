# LocalDrop — Planned Features

## 1. Copy-to-Clipboard on Received Links
Add a copy button next to each received link instead of just a plain anchor tag.
No backend changes needed — purely frontend using the Clipboard API.

## 2. File Deletion
Let the user remove individual files from the received sections and delete them from disk.
Requires a DELETE route on the backend and a remove button on each file card.

## 3. Duplicate Filename Handling
Right now if you send `photo.jpg` twice, the second upload silently overwrites the first.
Fix by appending a counter or timestamp to the filename on conflict e.g. `photo_1.jpg`.

## 4. Persist Data Across Restarts
All files and links reset when the service restarts because everything is stored in memory.
Use SQLite (via Python's built-in `sqlite3`) to store filenames and links in a local DB file
so history survives restarts.

## 5. File Size and Timestamp on File Cards
Show the file size and the time it was received under each file in the received section.
Requires storing metadata (size, timestamp) alongside the filename.

## 6. Upload Progress Indicator
Right now there is no feedback while a large file is uploading — the button just sits there.
Add a progress bar using the `XMLHttpRequest` upload progress event.

## 7. Download All as ZIP
A single button that zips everything in the received section and downloads it at once.
Requires a backend route that uses Python's `zipfile` module to bundle the files.

## 8. PIN Protection for /connect
Anyone on the same Wi-Fi can visit the IP directly without scanning the QR.
Add a simple PIN or passphrase check on the `/connect` route so only someone with the PIN
can access the phone page.

## 9. Rate Limiting on Uploads
Prevent someone on the network from flooding the disk with rapid uploads.
Use Flask-Limiter to cap upload requests per IP per minute.

## 10. Multi-Device Support
Right now only one phone can be connected at a time.
Expand to a session model where multiple devices connect with their own isolated
send/receive queues identified by a session token set at `/connect`.

## 11. Browser Notifications on the Desktop
Notify the desktop user when a file or link arrives from the phone using the
Web Notifications API — no need to keep the browser tab in focus.

## 12. Auto-Clear Old Files
Automatically delete files from the `uploads/` folder after a configurable number of days
to prevent unbounded disk growth. Can be implemented as a background cleanup thread.
