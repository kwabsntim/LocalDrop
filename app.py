from flask import Flask, render_template
import socket 



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




#routes for the application
@app.route("/")
def hello_world():
    return render_template('index.html',qr_code_data=get_local_ip())



if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')