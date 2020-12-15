from flask import Flask, render_template, request


app = Flask(__name__)

translite_dict = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I',
    'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
    'Х': 'KH', 'Ц': 'TC', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ы': 'Y', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA',
}


@app.route('/', methods=['post', 'get'])
def login():
    transliter = ''
    if request.method == 'POST':
        word = request.form.get('word')

        for alpha in word:
            if alpha.isalpha():
                transliter += translite_dict[alpha.upper()]
            else:
                transliter += alpha

    return render_template('index.html', message=transliter.title())


if __name__ == '__main__':
    app.run()