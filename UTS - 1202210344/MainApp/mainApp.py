from flask import Flask, jsonify, render_template, redirect, url_for, request
import requests
from requests.exceptions import HTTPError, JSONDecodeError

app = Flask(__name__)

# layanan penjualan
def post_penjualan(data):
    url = 'http://localhost:5000/create-penjualan/'
    response = requests.post(url, json=data)
    return response.json()

def get_penjualan(PenjualanID=None):
    url = 'http://localhost:5000/show-penjualan/'
    if PenjualanID is not None:
        url += str(PenjualanID)
    response = requests.get(url)
    return response.json()

def update_penjualan(PenjualanID, data):
    url = f'http://localhost:5000/update-penjualan/{PenjualanID}'
    response = requests.put(url, json=data)
    return response.json()

def delete_penjualan(PenjualanID):
    url = f'http://localhost:5000/delete-penjualan/{PenjualanID}'
    response = requests.delete(url)
    return response.json()

# layanan produk
""" def post_produk(data):
    url = 'http://localhost:5001/produk'
    response = requests.post(url, json=data)
    return response.json() """

""" def get_produk(ProdukID=None):
    url = 'http://localhost:5001/produk/'
    if ProdukID is not None:
        url += str(ProdukID)
    response = requests.get(url)
    return response.json() """
    
def post_produk(data):
    url = 'http://localhost:5001/produk/'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise HTTPError for non-2xx responses
        return response.json()  # Return decoded JSON data
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def get_produk(ProdukID=None):
    url = 'http://localhost:5001/produk/'
    if ProdukID is not None:
        url += str(ProdukID)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for non-2xx responses
        return response.json()  # Return decoded JSON data
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return []

def get_harga_produk(ProdukID):
    produk = get_produk(ProdukID)
    return produk['Harga'] if produk else None

def update_produk(ProdukID, data):
    url = f'http://localhost:5001/produk/{ProdukID}'
    response = requests.put(url, json=data)
    return response.json()

def delete_produk(ProdukID):
    url = f'http://localhost:5001/produk/{ProdukID}'
    response = requests.delete(url)
    return response.json()

# Routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-penjualan', methods=['GET', 'POST'])
def create_penjualan():
    if request.method == 'POST':
        data = request.form.to_dict()
        produkID = data['ProdukID']
        harga_produk = get_harga_produk(produkID)
        if harga_produk is None:
            return "Produk tidak ditemukan"
        
        total_harga = int(data['Jumlah']) * harga_produk
        data['TotalHarga'] = total_harga
        create_penjualan_data = post_penjualan(data)
        return redirect(url_for('get_penjualan_info', PenjualanID=create_penjualan_data['PenjualanID'], ProdukID=produkID))
    return render_template('CreatePenjualan.html')

@app.route('/show-penjualan')
def get_penjualan_list():
    penjualan_list = get_penjualan()
    return render_template('PenjualanList.html', detail=penjualan_list)

@app.route('/show-penjualan/<int:PenjualanID>')
def get_penjualan_info(PenjualanID):
    penjualan = get_penjualan(PenjualanID)
    return render_template('DetailPenjualan.html', detail=penjualan)

@app.route('/update-penjualan/<int:PenjualanID>', methods=['GET', 'POST'])
def update_penjualan_info(PenjualanID):
    if request.method == 'POST':
        data = request.form.to_dict()
        update_penjualan_data = update_penjualan(PenjualanID, data)
        return redirect(url_for('get_penjualan_info', PenjualanID=update_penjualan_data['PenjualanID']))
    penjualan = get_penjualan(PenjualanID)
    return render_template('UpdatePenjualan.html', detail=penjualan)

@app.route('/delete-penjualan/<int:PenjualanID>')
def delete_penjualan_info(PenjualanID):
    delete_penjualan_data = delete_penjualan(PenjualanID)
    return redirect(url_for('get_penjualan_list', PenjualanID=delete_penjualan_data['PenjualanID']))

@app.route('/create-produk', methods=['GET', 'POST'])
def create_produk():
    if request.method == 'POST':
        try:
            produk_id = request.form['ProdukID']
            nama = request.form['Nama']
            kategori = request.form['Kategori']
            harga = round(float(request.form['Harga']), 2)
            kadaluarsa = request.form['Kadaluarsa']
            
            if produk_id and nama and kategori and harga and kadaluarsa:  
                data = {
                    'ProdukID': produk_id,
                    'Nama': nama,
                    'Kategori': kategori,
                    'Harga': harga,
                    'Kadaluarsa': kadaluarsa
                }
                create_produk_data = post_produk(data)
                return redirect(url_for('get_produk_info', ProdukID=data['ProdukID']))
            else:
                return "Failed to create Produk"
        except ValueError:
            return "Harga harus berupa angka" 
    return render_template('CreateProduk.html')

@app.route('/show-produk')
def get_produk_list():
    produk_list = get_produk()
    return render_template('ProdukList.html', result=produk_list) 

@app.route('/show-produk/<int:ProdukID>')
def get_produk_info(ProdukID):
    produk_detail = get_produk(ProdukID)
    return render_template('DetailProduk.html', result=produk_detail)

@app.route('/update-produk/<int:ProdukID>', methods=['GET', 'POST'])
def update_produk_info(ProdukID):
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            update_produk(ProdukID, data)
            return redirect(url_for('get_produk_info', ProdukID=ProdukID))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    produk_detail = get_produk(ProdukID)
    return render_template('UpdateProduk.html', result=produk_detail)

@app.route('/delete-produk/<int:ProdukID>')
def delete_produk_info(ProdukID):
    delete_produk_data = delete_produk(ProdukID)
    if 'ProdukID' in delete_produk_data:
        return redirect(url_for('get_produk_list'))
    else:
        return "Error: ProdukID not found in delete_produk_data"


if __name__ == "__main__":
    app.run(debug=True, port=5003)
