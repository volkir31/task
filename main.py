from flask import Flask, render_template, request, jsonify
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///LevelDB.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

base = declarative_base()
base.query = session.query_property()

from models import *

base.metadata.create_all(bind=engine)

translite_dict = {

    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I',
    'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
    'Х': 'KH', 'Ц': 'TC', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ы': 'Y', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA',
}


def translite(word):
    transliter = ''
    for alpha in word:
        if alpha.isalpha():
            transliter += translite_dict[alpha.upper()]
        else:
            transliter += alpha
    return transliter.title()


@app.route('/', methods=['post', 'get'])
def main():
    return render_template('index.html')


data = []


@app.route('/translite', methods=['GET', 'POST'])
def get_len():
    word = ''
    if request.method == 'POST':
        word = request.form.get('word')
    return translite(word)


@app.route('/api', methods=['GET'])
def get_json():
    return jsonify(data)


@app.route('/api', methods=['POST'])
def update_json():
    new_json = request.json
    out_json = {"status": "success", 'data': translite(new_json['data'])}
    d = LevelDB(data=new_json['data'], transliter=translite(new_json['data']))
    session.add(d)
    session.commit()
    data.append(out_json)
    return jsonify(data[-1])


@app.route('/history')
def show_history():
    border = int(request.args['n'])
    out_list = []
    v = LevelDB.query.all()
    try:
        for index in range(border):
            out_list.append({'data': v[index].data, 'transliter': v[index].transliter})
        return render_template('history.html', content=out_list)
    except IndexError:
        out_list.append([f'В базе всего {len(v)} записей'])
        for index in range(len(v)):
            out_list.append({'data': v[index].data, 'transliter': v[index].transliter})
        return render_template('history.html', content=out_list)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
