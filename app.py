import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, session, request

from config import Configuration

app = Flask(__name__)
app.secret_key = b"\xf5j:.T8\x1c\xd2\x9d72\xeb\x00'=D"

config = Configuration()
config.load_file('/home/flask/manage_nginx_host/config.json')
# config.load_file('C:/flask/config.json')


@app.route('/')
def home():
    if 'member' not in session:
        return redirect(url_for('login_view'))

    body = render_template('index.html')
    return body


@app.route('/member/login', methods=['GET'])
def login_view():
    if 'member' in session:
        return redirect(url_for('home'))

    body = render_template('member/login.html')
    return body


@app.route('/member/login', methods=['POST'])
def login_action():
    try:
        if valid_login(request.form['email'], request.form['password']):
            return redirect(url_for('home'))
        else:
            return get_message('Invalid Email/Password'), 400
    except KeyError:
        return get_message('Invalid Email/Password'), 500


def valid_login(email, password):
    if email == 'duveen@duveen.me' and password == '1234':
        session['member'] = {'name': email, 'password': password}
        return True

    return False


@app.route('/member/logout')
def logout():
    session.pop('member')
    return redirect(url_for('login_view'))


@app.route('/restartNginx', methods=['POST'])
def restart_nginx():
    if 'member' not in session:
        return redirect(url_for('login_view'))

    resCode = os.system('systemctl restart nginx')
    
    if resCode == 256:
        return {'result': "Failed"}, 500

    return {'result': "Success"}, 200


@app.route('/host')
def host_list():
    if 'member' not in session:
        return redirect(url_for('login_view'))

    files = scan_files(config.base_dir)
    return render_template('host/host_list.html', len=len(files), files=files)


@app.route('/host/<path:host_file>')
def host_file_detail(host_file):
    if 'member' not in session:
        return redirect(url_for('login_view'))

    host_file_str = host_file
    path = os.path.abspath(config.base_dir) + "/" + host_file

    if os.path.isdir(path):
        files = scan_files(path)
        return render_template('host/host_list.html', len=len(files), files=files)

    with open(path, 'r', encoding="UTF8") as host_file:
        try:
            host_content = host_file.read(os.path.getsize(path))
        except UnicodeDecodeError:
            return get_message("This file cannot be read.")

    return render_template('host/host_file.html', host_file=host_file_str, host_content=host_content)


@app.route('/host/<path:host_file>', methods=['POST'])
def host_file_save(host_file):
    if 'member' not in session:
        return redirect(url_for('login_view'))

    path = os.path.abspath(config.base_dir) + "/" + host_file
    if os.path.isdir(path):
        return get_message('Not allowed modify directory!'), 400

    host_content = str(request.form['host_content']).replace('\r\n', '\n')

    os.rename(path, path + '.bak')

    with open(path, 'x+', encoding="UTF8") as copy_file:
        copy_file.write(host_content)

    os.remove(path + '.bak')

    return get_message("Success Saved!"), 200


def scan_files(base_dir):
    files = []
    for file in os.scandir(base_dir):
        stat = file.stat()

        file_info = {'init': ''}
        file_info.clear()

        file_info['name'] = file.name
        file_info['size'] = format(stat.st_size, ',')
        file_info['modified'] = convert_date(stat.st_mtime)

        files.append(file_info)

    return files


def convert_date(timestamp):
    d = datetime.fromtimestamp(timestamp)
    formated_date = d.strftime('%Y-%b-%d')
    return formated_date


def get_message(msg):
    return '''<script>
    alert("''' + msg + '''");
    history.back();
    </script>'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8200)
