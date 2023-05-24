from flask import Flask, render_template, request
from ssind import capture_screenshots, generate_pdf_report

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    config = request.form.get('config')
    clear = request.form.get('clear') == 'true'
    capture_screenshots(clear, config)
    generate_pdf_report('screenshots')
    return 'Screenshots captured and PDF report generated!'

if __name__ == '__main__':
    app.run()