# -*- coding: utf-8 -*-

import flask
import predict
import util

import json
import os


app = flask.Flask(__name__)
app.debug = True


@app.route('/predict', methods=['GET'])
def main():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(this_dir, 'data', 'alegre')
    train_dir = os.path.join(this_dir, 'model', 'alegre')

    # restore config
    config = util.load_from_dump(os.path.join(train_dir, 'flags.cPickle'))
    config['data_dir'] = data_dir
    config['train_dir'] = train_dir

    text = flask.request.args.get('text')
    res = {}
    result = predict.predict(text, config, raw_text=True)
    language_codes = util.load_language_codes()
    res['prediction'] = language_codes[result['prediction']]
    res['scores'] = {language_codes[k]: v for k, v in result['scores'].iteritems()}
    return json.dumps(res, ensure_ascii=False, indent=2)


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'docs', 'img'),
                                     'favicon.ico', mimetype='image/png')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


if __name__ == '__main__':
    app.run()
