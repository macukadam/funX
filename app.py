from flask import Flask, render_template, request
import requests as r
from autometrics import autometrics
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')


@app.post('/search')
@autometrics
def search():
    search_term = request.form.get('search')
    if not search_term or len(search_term) < 3:
        return ''

    url = f'https://api.github.com/search/repositories?q={search_term}'
    response = r.get(url)
    return render_template('search_results.html', data=response.json())


@app.route('/fetch-contributor')
@autometrics
def fetch_contributor():
    login = request.args.get('login')
    if not login:
        return "Login not provided", 400

    url = f'https://api.github.com/users/{login}'
    response = r.get(url)
    if response.status_code != 200:
        return "Error fetching contributor details", 500

    data = response.json()
    return render_template('contributor_profile.html', data=data)


@app.get("/")
@autometrics
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

