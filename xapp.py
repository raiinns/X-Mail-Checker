from flask import Flask, render_template, request
import requests

app = Flask(__name__)

class ChecK:
    def __init__(self, email):
        self.email = email
        self.status = self.twitter()

    def twitter(self):
        r = requests.Session()
        url = f"https://api.twitter.com/i/users/email_available.json?email={self.email}"
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
        r.headers.update({
            'User-Agent': user_agent,
            'Host': "api.twitter.com",
            'Accept': ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                       "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
        })
        try:
            req = r.get(url).json()
            if req.get('valid') == False:
                return "Linked"
            else:
                return "Unlinked"
        except Exception as e:
            return f"Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        emails = request.form['emails'].splitlines()  # Mengambil email per baris
        results = []
        for email in emails:
            checker = ChecK(email)  # Cek status email menggunakan class ChecK
            results.append(f"{email} = {checker.status}")
        return render_template('index.html', emails=request.form['emails'], results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
