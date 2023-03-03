import os
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))

def start_stream(stream_key):
    # Start the video stream with the given stream key
    command = "raspivid -o - -t 0 -n -w 720 -h 480 -fps 25 -b 2000000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/" + stream_key
    video_stream = os.popen(command)
    print("Stream started successfully.")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/start_stream', methods=['POST'])
def start():
    stream_key = request.form.get('stream_key')
    if not stream_key:
        with open(os.path.join(base_path, "stream_key.txt"), "r") as fp:
            stream_key = fp.read().strip()
        if not stream_key:
            return jsonify({'error': 'Stream key not provided and could not be read from file.'})
    else:
        with open(os.path.join(base_path, "stream_key.txt"), "w") as fp:
            fp.write(stream_key)
    start_stream(stream_key)
    return jsonify({'message': 'Stream started successfully.'})

if __name__ == '__main__':
    # Check if a valid stream key is present in the file
    with open(os.path.join(base_path, "stream_key.txt"), "r") as fp:
        stream_key = fp.read().strip()
    if stream_key:
        # Start the stream automatically
        start_stream(stream_key)
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)
