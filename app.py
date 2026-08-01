from flask import Flask, render_template,redirect,request,flash,url_for,send_from_directory
from werkzeug.utils import secure_filename
import socket 
import qrcode
import io
import base64
import os
import time
from config import config


#this variable determines if the phone is connected or not
phone_connected=False
connection_time=None
manually_disconnected=False  # blocks polling from auto-reconnecting
CONNECTION_TIMEOUT=300  # 5 minutes

Recieved_links=[]      # links sent from phone → shown on desktop
desktop_links=[]       # links sent from desktop → shown on phone

# Track file origin: phone_files = uploaded from phone (shown on desktop)
#                   desktop_files = uploaded from desktop (shown on phone)
phone_files=[]
desktop_files=[]

#importing the config file

env=os.getenv('FLASK_ENV','development')
app_config=config[env]

app = Flask(__name__)
app.config.from_object(app_config)
app.secret_key='LocalDrop'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#user functions 
def get_local_ip():
    '''
     get the local ip address of device to generat the qr code for the connection
    '''
    s=None
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip =socket.gethostbyname(socket.gethostname())
    finally:
        if s:
            s.close()
    if local_ip.startswith("127.") or local_ip=="0.0.0.0":
        return "could not determine a non-loopback IP address"
    return local_ip

#Qr code  function 
def generate_qr_code(data):
    ''''
    Generate a QR code from the provided data and return it as a base64-encoded string.
    '''

    qr=qrcode.QRCode(version=1,box_size=10,border=4,error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make(fit=True)

    #making the qr code image 
    img=qr.make_image(fill_color="black",back_color="white")

    #save the image to the buffer

    buffer=io.BytesIO()
    img.save(buffer,format="PNG")
    buffer.seek(0)

    #encode the image to base64
    img_bytes=buffer.read()
    base64_bytes=base64.b64encode(img_bytes)

    base64_string=base64_bytes.decode('utf-8')
    return base64_string

def allowed_file(filename):
    '''
    Check if the uploaded file has an allowed extension.
    '''
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



#routes for the application
@app.route("/")
def hello_world():
    data="http://"+get_local_ip()+":"+str(app_config.PORT)+"/connect"
    qr_base64=generate_qr_code(data)
    files=os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
    return render_template('index.html',qr_code_img=qr_base64,files=files)
def add(a, b):
    return a + b
#this route is to determine a phone connection
@app.route("/connect")
def connect():
    global phone_connected, connection_time, manually_disconnected
    phone_connected=True
    connection_time=time.time()
    manually_disconnected=False
    return render_template('connect.html', files=desktop_files, links=desktop_links)

@app.route("/disconnect", methods=['POST'])
def disconnect():
    global phone_connected, connection_time, manually_disconnected
    phone_connected = False
    connection_time = None
    manually_disconnected = True
    return '', 204

@app.route("/nav_status")
def nav_status():
    global phone_connected, connection_time
    if phone_connected and connection_time:
        if time.time() - connection_time > CONNECTION_TIMEOUT:
            phone_connected = False
            connection_time = None
    if phone_connected:
        return '''<span class="nav-badge">
            <span class="nav-dot"></span>Active
            <label class="toggle-switch" title="Disconnect device">
                <input type="checkbox" checked
                       hx-post="/disconnect"
                       hx-swap="none"
                       hx-trigger="change">
                <span class="toggle-slider"></span>
            </label>
        </span>'''
    return ''

#the status route is the laptops transfer page and it also checks if the phone is connected or not and updates the page accordingly
@app.route("/status")
def status():
    global phone_connected, connection_time
    
    # Check if connection has timed out
    if phone_connected and connection_time:
        if time.time() - connection_time > CONNECTION_TIMEOUT:
            phone_connected = False
            connection_time = None
    
    if phone_connected==False:
        # Generate fresh QR code for polling
        data="http://"+get_local_ip()+":"+str(app_config.PORT)+"/connect"
        qr_base64=generate_qr_code(data)
        return f'''<div id="main-content"
                    hx-get="/status"
                    hx-trigger="every 2s"
                    hx-swap="outerHTML">
                    <p style="color: white; text-align: center; font-size: 1.2rem; margin-bottom: 20px;">Scan the QR Code to connect a device</p>
                    <img src="data:image/png;base64,{qr_base64}" alt="QR Code" style="max-width: 300px; margin: 0 auto; display: block;" />
                </div>'''
    
    files=os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
    # Return only the content to be swapped by HTMX, not a full page
    return render_template('status_content.html',phone_connected=phone_connected,links=Recieved_links,files=phone_files)
    


@app.route("/upload",methods=['POST'])
def upload_file():
    global phone_files, desktop_files
    referrer = request.referrer or ''
    came_from_phone = '/connect' in referrer
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if 'file' not in request.files or request.files['file'].filename == '':
        if is_ajax:
            return {'ok': False, 'message': 'No file selected'}, 400
        return redirect(referrer or '/')

    file = request.files['file']
    if not allowed_file(file.filename):
        if is_ajax:
            return {'ok': False, 'message': 'File type not allowed'}, 400
        return redirect(referrer or '/')

    filename = secure_filename(file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if came_from_phone:
        if filename not in phone_files:
            phone_files.append(filename)
    else:
        if filename not in desktop_files:
            desktop_files.append(filename)

    if is_ajax:
        msg = 'File sent to desktop!' if came_from_phone else 'File sent to phone!'
        return {'ok': True, 'message': msg}
    return redirect('/connect' if came_from_phone else '/')


@app.route("/send_link",methods=['POST'])
def send_link():
    global Recieved_links, desktop_links
    referrer = request.referrer or ''
    came_from_phone = '/connect' in referrer
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if 'link' not in request.form or not request.form['link'].strip():
        if is_ajax:
            return {'ok': False, 'message': 'No link provided'}, 400
        return redirect(referrer or '/')

    link = request.form['link'].strip()
    if came_from_phone:
        Recieved_links.append(link)
    else:
        desktop_links.append(link)

    if is_ajax:
        msg = 'Link sent to desktop!' if came_from_phone else 'Link sent to phone!'
        return {'ok': True, 'message': msg}
    return redirect('/connect' if came_from_phone else '/')


@app.route("/phone_updates")
def phone_updates():
    '''Returns just the received files + links sections for the phone to poll'''
    global phone_connected, connection_time, manually_disconnected
    # Only keep connection alive if it wasn't manually disconnected
    if not manually_disconnected:
        phone_connected = True
        connection_time = time.time()
    return render_template('phone_updates.html', files=desktop_files, links=desktop_links)

@app.route("/updates_status")
def update_status():
    if phone_connected==False:
        return '',204
    files=os.listdir(app.config['UPLOAD_FOLDER'])    
    return render_template('updates.html',phone_connected=phone_connected,links=Recieved_links,files=files)

@app.route("/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], secure_filename(filename))

if __name__ == '__main__':
    app.run(debug=app_config.DEBUG, port=app_config.PORT, host=app_config.HOST)