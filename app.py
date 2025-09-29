from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v18.0/{thread_id}/comments?access_token={access_token}'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f" Sent from token {access_token}: {message}")
                else:
                    print(f" Failed from token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f' Commenting started with Task ID: {task_id}'

    return render_template_string(html_template)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f' Commenting Task with ID {task_id} stopped.'
    else:
        return f' No task found with ID {task_id}.'

# Premium HTML Template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AYUSH XWD </title>

  <!-- Bootstrap -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
  <!-- Font Awesome -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

  <style>
    body {
      min-height: 100vh;
      margin: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #0f0f0f, #1a1a2e, #000000);
      font-family: 'Orbitron', sans-serif;
      color: #fff;
      overflow-x: hidden;
    }

    .neon-bg {
      position: absolute;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,0,0,0.3) 0%, transparent 70%),
                  radial-gradient(circle, rgba(0,255,255,0.2) 0%, transparent 80%);
      background-size: 50% 50%;
      animation: move-bg 10s linear infinite;
      z-index: -1;
    }

    @keyframes move-bg {
      0% { transform: translate(0, 0); }
      50% { transform: translate(-25%, -25%); }
      100% { transform: translate(0, 0); }
    }

    .glass-card {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      box-shadow: 0 0 40px rgba(255, 0, 0, 0.6);
      backdrop-filter: blur(15px);
      padding: 30px;
      width: 100%;
      max-width: 450px;
      animation: fadeIn 1s ease-in-out;
    }

    .header h1 {
      font-size: 60px;
      font-weight: 700;
      color: #ff4d4d;
      text-shadow: 0 0 20px red, 0 0 40px #ff1a1a;
      margin-bottom: 20px;
    }

    label {
      font-size: 14px;
      letter-spacing: 1px;
      color: #ffb3b3;
    }

    .form-control {
      background: transparent;
      border: 2px solid #ff4d4d;
      color: #fff;
      border-radius: 12px;
      font-size: 15px;
      padding: 10px;
      transition: 0.3s;
    }
    .form-control:focus {
      border-color: #ff1a1a;
      box-shadow: 0 0 15px red;
    }
    .form-control::placeholder {
      color: #aaa;
    }

    .btn-red {
      background: linear-gradient(90deg, #ff4d4d, #ff1a1a);
      border: none;
      border-radius: 12px;
      font-weight: bold;
      color: #000;
      padding: 10px;
      transition: 0.3s;
      width: 100%;
      letter-spacing: 1px;
    }
    .btn-red:hover {
      background: linear-gradient(90deg, #ff1a1a, #cc0000);
      color: #fff;
      box-shadow: 0 0 15px #ff1a1a;
    }

    .footer {
      margin-top: 20px;
      font-size: 16px;
      color: #ff4d4d;
      text-align: center;
    }
    .footer a {
      margin: 0 12px;
      color: #25d366;
      transition: 0.3s;
    }
    .footer a.facebook-link {
      color: #1877f2;
    }
    .footer a:hover {
      text-shadow: 0 0 10px currentColor;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }
  </style>
</head>
<body>
  <div class="neon-bg"></div>

  <div class="header text-center">
    <h1>AYUSH XWD</h1>
  </div>

  <div class="glass-card">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">Select Token Option</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">Paste Single Token</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">Choose Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Enter Post UID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Enter Your Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Time Interval (Sec)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Choose NP File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-red"> Start</button>
    </form>

    <form method="post" action="/stop" class="mt-4">
      <div class="mb-3">
        <label for="taskId" class="form-label">Enter Task ID to Stop</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-red"> Stop</button>
    </form>
  </div>

  <footer class="footer">
    <p>� OWNER AYUSH P9NDIT </p>
    <a href="https://www.facebook.com/profile.php?id=61578840652817" class="facebook-link"><i class="fab fa-facebook"></i> Facebook</a>
    <a href="https://wa.me/+919174751272"><i class="fab fa-whatsapp"></i> WhatsApp</a>
  </footer>

  <script>
    function toggleTokenInput() {
      const tokenOption = document.getElementById('tokenOption').value;
      document.getElementById('singleTokenInput').style.display = tokenOption === 'single' ? 'block' : 'none';
      document.getElementById('tokenFileInput').style.display = tokenOption === 'multiple' ? 'block' : 'none';
    }
  </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
