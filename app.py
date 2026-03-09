from flask import Flask, render_template
import socket 
import qrcode
import io
import base64


app = Flask(__name__)

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


data=get_local_ip()
qr_base64=generate_qr_code(data)


#routes for the application
@app.route("/")
def hello_world():
    return render_template('index.html',qr_code_img=qr_base64)



if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')