from dust.application import Application
from dust.responses import JsonResponse, HtmlResponse
import os

app = Application()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_uploaded_file(file_data, upload_folder):
    filename = file_data['filename']
    filepath = os.path.join(upload_folder, filename)
    with open(filepath, 'wb') as f:
        f.write(file_data['content'])

    return filename

@app.route('/', methods=['GET'])
def home(request):
    return HtmlResponse("<h1>Welcome to Dust Framework!</h1>")

@app.route('/hello', methods=['GET'])
def hello(request):
    return "Hello, World!"

@app.route('/json', methods=['GET'])
def json_example(request):
    data = {"message": "This is a JSON response"}
    return JsonResponse(data)

@app.route('/data', methods=['POST'])
def post_data(request):
    return "Data received via POST"

@app.route('/update', methods=['PUT'])
def update_data(request):
    return "Data received via PUT"

@app.route('/delete', methods=['DELETE'])
def delete_data(request):
    return "Data received via DELETE"

@app.route('/upload', methods=['POST'])
def upload_file(request):
    if 'file' not in request.form:
        return "No file part in the request"
    
    file_data = request.form['file']
    filename = file_data['filename']
    filepath = save_uploaded_file(file_data, UPLOAD_FOLDER)

    return f"File {filename} uploaded successfully"

@app.websocket('/ws')
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
