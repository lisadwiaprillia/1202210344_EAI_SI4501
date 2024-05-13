from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Provide your MySQL password here
    database="uts_eai"
)

# Function to close database connection
def close_db_connection(cursor):
    cursor.close()

@app.route('/')
def root():
    return 'Selamat Datang di Manajemen Produk'

@app.route('/produk/', methods=['GET', 'POST'])
def produk():
    cursor = db.cursor(dictionary=True)
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM produk")
            data = cursor.fetchall()
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'POST':
        try:
            data = request.json
            sql = "INSERT INTO produk (ProdukID, Nama, Kategori, Harga, Kadaluarsa) VALUES (%s, %s, %s, %s, %s)"
            val = (data['ProdukID'], data['Nama'], data['Kategori'], data['Harga'], data['Kadaluarsa'])
            cursor.execute(sql, val)
            db.commit()
            return jsonify({'message': 'Data Berhasil Ditambahkan'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

@app.route('/produk/<int:ProdukID>', methods=['GET', 'DELETE', 'PUT'])
def detailproduk(ProdukID):
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM produk WHERE ProdukID = %s", (ProdukID,))
            data = cursor.fetchone()
            if data:
                return jsonify(data)
            else:
                return jsonify({'message': 'produk tidak ditemukan'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM produk WHERE ProdukID = %s", (ProdukID,))
            db.commit()
            return jsonify({'ProdukID': ProdukID, 'message': 'Data Berhasil Dihapus'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'PUT':
        try:
            data = request.json
            sql = "UPDATE produk SET Nama=%s, Kategori=%s, Harga=%s, Kadaluarsa=%s WHERE ProdukID = %s"
            val = (data['Nama'], data['Kategori'], data['Harga'], data['Kadaluarsa'], ProdukID)
            cursor.execute(sql, val)
            db.commit()
            return jsonify({'message': 'Data Berhasil Diupdate'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
