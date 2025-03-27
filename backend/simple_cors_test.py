from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enklast möjliga CORS-konfiguration
CORS(app)

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)