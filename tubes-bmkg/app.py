from flask import Flask, render_template, request
import requests
from functools import reduce

# inisialisasi object flask nama varibale bebas disini pake app jadi nanti seteurs nya harus pake app juga contoh @app.route
app = Flask(__name__)

# fungsi untuk mengambil data dari api dan mengkonversi kan ke dalam json
def get_api(url):
    data = ''
    url = url
    data =requests.get(url).json()
    return data

# fungsi untuk menghitung rata rata kekuatan 15 gempat terakhir  menggunakan lambda dan reduce
def rata_rata(data):
    kekuatan_gempa = []
    for gempa_dirasakan in data['Infogempa']['gempa']:
        kekuatan_gempa.append(float(gempa_dirasakan['Magnitude']))

    rata_rata_gempa  = reduce(lambda x, y : x + y, kekuatan_gempa) / len(kekuatan_gempa)
    return round(rata_rata_gempa, 1)

#app route -> untuk routing atau url nya di bawah route itu fungsi atau method nya
@app.route('/')
def home():

    data                 =  get_api('https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json')
    data_gempa_dirasakan = get_api('https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json')

    data_gempa      = data['Infogempa']['gempa']
    gempa_dirasakan = data_gempa_dirasakan['Infogempa']['gempa']

    rata_rata_gempa = rata_rata(data_gempa_dirasakan)

    # render template buat templating html
    return  render_template('home.html', data = data_gempa, gempa_dirasakan = gempa_dirasakan, rata_rata_gempa = rata_rata_gempa)

@app.route('/gempabumi-terkini', methods=['GET','POST'])
def gempabumi_terkini():

    data = get_api('https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json')

    if request.method == 'POST':

        if request.form.get('filter') == None:
            return 'Pilih opsi terlebih dahulu'

        # sorting data dengan menggunakan method sorted dan lambda
        data_gempa = sorted(data['Infogempa']['gempa'], key=lambda d: d[request.form['filter']], reverse=True)
    else:
        data_gempa = data['Infogempa']['gempa']

    return render_template('gempabumi_terkini.html', data = data_gempa)


# baris kode untuk debugging jadi kalo abis ngedit code ga perlu falain flask run terus
if __name__ == "__main__":
    app.run(debug=True)
