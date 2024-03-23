from flask import Flask, render_template, request, redirect, session
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
model = joblib.load('sambb.pkl')

# Dummy user database for login
user_database = {'sam': '1234', 'james': '1234', 'peter': '1234'}

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in user_database:
        return render_template('login.html', info='Invalid User')
    else:
        if user_database[name1] != pwd:
            return render_template('login.html', info='Invalid Password')
        else:
            # Set the username in the session
            session['username'] = name1
            return redirect('/home')  # Redirect to home page

@app.route('/home')
def home():
    username = session.get('username')
    if username:
        return render_template('home.html', name=username)
    else:
        return redirect('/')

@app.route('/predict', methods=['POST'])
def predict():
    try:
         # Get the input values from the form and convert them to float
        patient_name = request.form['name']
        session['patient_name'] = patient_name

        age = float(request.form['age'])
        sex = float(request.form['sex'])
        cp = float(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        restecg = float(request.form['restecg'])
        thalach = float(request.form['thalach'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])

        # Make a prediction using the loaded model
        prediction = model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        # Redirect to the appropriate page based on the prediction
        if prediction[0] == 1:
            return redirect('/heart_disease_page')
        else:
            return redirect('/no_heart_disease_page')


    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred during prediction."

@app.route('/heart_disease_page')
 
def heart_disease_page():
    patient_name = session.get('patient_name', 'the patient')
    information_for_heart_disease = f"This page contains information for {patient_name} with heart disease. Please follow the recommendations."
    return render_template('heart_disease_page.html', info=information_for_heart_disease, patient_name=patient_name)

@app.route('/no_heart_disease_page')
def no_heart_disease_page():
    patient_name = session.get('patient_name', 'the patient')
    information_for_no_heart_disease = f"This page contains information for {session.get('username', 'the patient')} without heart disease. Please consult with a healthcare professional for personalized advice."
    return render_template('no_heart_disease_page.html', info=information_for_no_heart_disease, patient_name=patient_name)

if __name__ == '__main__':
    app.run(debug=True)
