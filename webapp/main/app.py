import os
import json
import click
from flask import Flask, jsonify

fields = ['personal', 'experience', 'skills', 'education', 'achievements']

app = Flask(__name__)
app.config.from_object(__name__)


def parse_cv(cv_path, field):
    """

    :param cv_path: path of the CV file
    :param field: given field to look it up in the cv file
    :return: a list cv_content which contains the content of the CV for the given field
    """
    cv_content = []
    found = False
    start_index = 0
    stop_index = 0
    if os.path.exists(cv_path):
        _, file_extension = os.path.splitext(cv_path)
        with open(cv_path) as fd:
            if file_extension == '.json':
                content = json.load(fd)
                content = content.get(field, '')
                if content:
                    cv_content.extend(content if isinstance(content, list) else [content])
            else:
                content = fd.read()

        if file_extension != '.json':
            content_list = content.split('\n')
            content_list = list(filter(lambda x: x != '', content_list))
            for index, item in enumerate(content_list):
                if item.isupper() and field in item.lower() and found is False:
                    found = True
                    start_index = index+1
                    continue
                if item.replace(' ', '').isupper() and found is True:
                    stop_index = index
                if start_index != 0 and stop_index != 0:
                    cv_content = content_list[start_index:stop_index]
                    break
            else:
                if found and stop_index == 0:
                    cv_content = content_list[start_index:]

    return cv_content


@app.cli.command('get')
@click.argument('field')
def get_details(field):
    result = parse_cv(cv_path=os.getenv('EXAMPLE_JSON'), field=field)
    click.echo(result)


@app.route('/', methods=['GET'])
def list_endpoints():
    return jsonify(endpoints=fields)


@app.route('/<string:label>', methods=['GET'])
def get_cv_label_content(label):
    result = parse_cv(cv_path=os.getenv('EXAMPLE_TXT'), field=label)
    app.logger.info(result)
    if not result:
        return jsonify({'error': f"Content for endpoint '{label}' not found"}), 404
    return jsonify(result=result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
