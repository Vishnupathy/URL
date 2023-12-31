import random
import string
from datetime import datetime, timedelta
from urllib.parse import urlparse

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)

app = Flask(__name__)
app.secret_key = 'l&Z1ly3aa!'

url_list = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc])

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    original_url = None
    expiration_time = None
    click_count = 0

    if request.method == 'POST':
        original_url = request.form['url']
        expiration_time = request.form.get('expiration_time', None)
        current_time = datetime.now()

        if not is_valid_url(original_url):
            flash('Invalid URL format! Please enter a URL like https://mustafaemresahin.com')
            return render_template('index.html', url_list=url_list)

        if original_url in url_list:
            existing_expiration_time = url_list[original_url].get('expiration_time')
            if existing_expiration_time:
                dt_object = datetime.strptime(existing_expiration_time, '%Y-%m-%dT%H:%M')
                if current_time > dt_object:
                    flash('This URL has already been shortened but has expired.')
                    return render_template('index.html', url_list=url_list)
            flash('This URL has already been shortened.')
            return render_template('index.html', url_list=url_list)

        if original_url not in url_list:
            short_url = generate_short_url()
            url_list[original_url] = {'short_url': short_url, 'expiration_time': expiration_time, 'click_count': 0}

        current_time = datetime.now()
        for original, data in url_list.items():
            if data['expiration_time']:
                dt_object = datetime.strptime(data['expiration_time'], '%Y-%m-%dT%H:%M')
                data['formatted_expiration_time'] = dt_object.strftime('%B %d, %Y, %H:%M %p')
                data['is_expired'] = current_time > dt_object

        return redirect(url_for('index'))

    return render_template('index.html', url_list=url_list)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    for original, data in url_list.items():
        if data['short_url'] == short_url:
            if data.get('expiration_time') and datetime.now() > datetime.strptime(data['expiration_time'], '%Y-%m-%dT%H:%M'):
                flash('URL has expired!')
                return render_template('index.html', url_list=url_list)
            data['click_count'] += 1
            return redirect(original)

    flash('URL not found!')
    return redirect(url_for('index'))

@app.route('/delete_url', methods=['POST'])
def delete_url():
    data = request.json
    short_url_to_delete = data.get('url')

    for original, data in list(url_list.items()): 
        if data['short_url'] == short_url_to_delete:
            del url_list[original]
            return jsonify({'success': True}), 200

    return jsonify({'success': False, 'message': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
