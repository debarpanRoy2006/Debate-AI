from flask import Flask, request, jsonify, render_template
import joblib  # For loading ML models
import numpy as np
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OAuth Setup
oauth = OAuth(app)

# Google Login
google = oauth.register(
    name="google",
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)

# Facebook Login
facebook = oauth.register(
    name="facebook",
    client_id="YOUR_FACEBOOK_APP_ID",
    client_secret="YOUR_FACEBOOK_APP_SECRET",
    authorize_url="https://www.facebook.com/dialog/oauth",
    access_token_url="https://graph.facebook.com/oauth/access_token",
    client_kwargs={"scope": "email"},
)

# Google Auth Route
@app.route("/auth/google")
def google_login():
    return google.authorize_redirect(url_for("google_callback", _external=True))

@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()
    return f"Hello, {user_info['name']}! Email: {user_info['email']}"

# Facebook Auth Route
@app.route("/auth/facebook")
def facebook_login():
    return facebook.authorize_redirect(url_for("facebook_callback", _external=True))

@app.route("/auth/facebook/callback")
def facebook_callback():
    token = facebook.authorize_access_token()
    user_info = facebook.get("https://graph.facebook.com/me?fields=id,name,email").json()
    return f"Hello, {user_info['name']}! Email: {user_info.get('email', 'No email provided')}"

if __name__ == "__main__":
    app.run(debug=True)



# Load the trained ML model
model = joblib.load("model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['features']  # Expecting a list of features
        prediction = model.predict([np.array(data)])
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)