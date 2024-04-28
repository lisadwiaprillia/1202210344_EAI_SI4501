from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tugas2_eai'
mysql = MySQL(app)

@app.route('/')
def root():
    return 'Selamat Datang di Manajemen Data Mahasiswa'

@app.route('/mahasiswa', methods=['GET', 'POST'])
def detailmahasiswa():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM mahasiswa")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        
        cursor.close()
        return jsonify(data)

    elif request.method == 'POST':
        id_mhs = request.json['id_mhs']
        nama = request.json['NamaMahasiswa']
        nim = request.json['NIM']
        email = request.json['Email']
        nohandphone = request.json['NoHandphone']
        alamat = request.json['Alamat']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO mahasiswa (id_mhs, NamaMahasiswa, NIM, Email, NoHandphone, Alamat) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id_mhs, nama, nim, email, nohandphone, alamat)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data Berhasil Ditambahkan'})

@app.route('/mahasiswa/<int:id_mhs>', methods=['GET', 'DELETE', 'PUT'])
def rinciankontak(id_mhs):
    cursor = mysql.connection.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM mahasiswa WHERE id_mhs = %s", (id_mhs,))
        data = cursor.fetchone()
        if data:
            column_names = [i[0] for i in cursor.description]
            result = dict(zip(column_names, data))
            return jsonify(result)
        else:
            return jsonify({'message': 'Mahasiswa tidak ditemukan'}), 404

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM mahasiswa WHERE id_mhs = %s", (id_mhs,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data Berhasil Dihapus'})

    elif request.method == 'PUT':
        data = request.get_json()
        sql = "UPDATE mahasiswa SET NamaMahasiswa=%s, NIM=%s, Email=%s, NoHandphone=%s, Alamat=%s WHERE id_mhs = %s"
        val = (data['NamaMahasiswa'], data['NIM'], data['Email'], data['NoHandphone'], data['Alamat'], id_mhs)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data Berhasil Diupdate'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
