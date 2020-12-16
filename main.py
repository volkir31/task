from flask import Flask, render_template, request, json

app = Flask(__name__)

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


@app.route('/translite', methods=['GET', 'POST'])
def get_len():
    word = ''
    if request.method == 'POST':
        word = request.form.get('word')
    return translite(word)


@app.route('/api')
def a():
    page = request.args.get('page', default=0, type=int)
    RE = 'page: ' + str(page) + '\n' + 'filter: ' + str(filter)
    return RE


@app.route('/add', methods=['POST'])
def add():
    f = request.json()
    return f


if __name__ == '__main__':
    app.run()
