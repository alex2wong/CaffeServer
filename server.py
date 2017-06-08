from flask import Flask, jsonify, request, abort, Response
from time import time
from uuid import uuid4
import json
import os
import sys
import imageop
import demo

app = Flask(__name__)

class Todo(object):
    def __init__(self, content):
        self.id = str(uuid4())
        self.content = content
        self.created_at = time()
        self.is_finished = False
        self.finished_at = None
    
    def finish(self):
        self.is_finished = True
        self.finished_at = time()
    
    def json(self):
        return json.dumps({
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'is_finished': self.is_finished,
            'finished_at': self.finished_at
        })


# config server route... need REST api
@app.route('/')
@app.route('/index')
def index():
    # return jsonify(msg='upload your image to classify')
    return "<h3>Upload your image to classify</h3>"

@app.route('/upload', methods=['POST'])
def addImage():
    for k in request.form:
        print("received form ele: " + k + ', ' + request.form[k])
    # content = request.form.get('file2upload', None)
    print(request.files)
    content = request.files['file2upload']
    if not content:
        abort(400)
    # save image to fileSys.
    imageName = content.filename
    print('Saving to filepath ./assets/' + imageName)
    content.save('./assets/' + imageName)
    # ready2 run image classify
    im_names = [imageName]
    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Test for data/demo/{}'.format(im_name)
        demo.imageClassify(demo.net, im_name)
    return jsonify(msg='upload success', imageurl='./assets/' + imageName)

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
    