import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = b"\xf5j:.T8\x1c\xd2\x9d72\xeb\x00'=D"


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
            return get_error_msg('Invalid Email/Password'), 400
    except KeyError:
        return get_error_msg('Invalid Email/Password'), 500


def valid_login(email, password):
    if email == 'duveen@duveen.me' and password == '1234':
        session['member'] = {'name': email, 'password': password}
        return True

    return False


@app.route('/member/logout')
def logout():
    session.pop('member')
    return redirect(url_for('login_view'))


@app.route('/hosts')
def host_list():
    if 'member' not in session:
        return redirect(url_for('login_view'))

    files = []
    for file in os.scandir('C:/BioData'):
        stat = file.stat()

        file_info = {'init': ''}
        file_info.clear()

        file_info['name'] = file.name
        file_info['size'] = format(stat.st_size, ',')
        file_info['modified'] = convert_date(stat.st_mtime)

        files.append(file_info)

    return render_template('host/list.html', len=len(files), files=files)


def convert_date(timestamp):
    d = datetime.fromtimestamp(timestamp)
    formated_date = d.strftime('%Y-%b-%d')
    return formated_date


def get_error_msg(msg):
    return '''<script>
    alert("''' + msg + '''");
    history.back();
    </script>'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8200)
