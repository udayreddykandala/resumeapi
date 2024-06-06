# app.py
from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, render_template
from data import education, experience, achievements, professional_summary, skills, professional_development
import os
from config import Config
import logging

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)

logging.basicConfig(level=logging.DEBUG)

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    app.logger.debug(f'Redirect URI: {redirect_uri}')
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    try:
        token = google.authorize_access_token()
        app.logger.debug(f'Token received: {token}')
        user_info = google.parse_id_token(token)
        app.logger.debug(f'User info received: {user_info}')
        session['user'] = user_info
        return redirect('/')
    except Exception as e:
        app.logger.error(f"Error during Google OAuth: {str(e)}", exc_info=True)
        return "An error occurred during authentication.", 500

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/')
def index():
    if 'user' in session:
        user_info = session['user']
        return f"Hello, {user_info['name']}!"
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/api/resume/education', methods=['GET'])
def get_education():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'education.html',
        education=education.education
    )

@app.route('/api/resume/experience', methods=['GET'])
def get_experience():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'professional_experience.html',
        experience=experience.experience
    )

@app.route('/api/resume/achievement', methods=['GET'])
def get_achievement():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'achievements.html',
        achievements=achievements.achievements
    )

@app.route('/api/resume/professional_summary', methods=['GET'])
def get_professional_summary():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'professional_summary.html',
        professional_summary=professional_summary.professional_summary
    )

@app.route('/api/resume/skills', methods=['GET'])
def get_skills():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'skills.html',
        skills=skills.skills['skills']
    )

@app.route('/api/resume/professional_development', methods=['GET'])
def get_professional_development():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'professional_development.html',
        professional_development=professional_development.professional_development
    )

if __name__ == '__main__':
    app.run(debug=True)
