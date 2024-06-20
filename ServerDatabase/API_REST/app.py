from flask import Flask, jsonify, request, abort, render_template, send_from_directory
import psycopg2
import os
from psycopg2.extras import RealDictCursor
import logging
import uuid

API_KEYS = os.environ.get('API_KEYS').split(',')

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = './static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para conectarse a la base de datos
def connect_db():
    conn = psycopg2.connect(
        host='timescaledb',  
        database= os.environ.get('POSTGRES_DB'),
        user= os.environ.get('POSTGRES_USER'),
        password= os.environ.get('POSTGRES_PASSWORD')
    )
    return conn


# Función para consultar los datos desde la base de datos
def simple_querry(query):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(query)
    data = cursor.fetchall()
    
    conn.close()
    return data


@app.route('/', methods=['GET'])
def get_index():    
    return jsonify("Try /data")

@app.route('/add', methods=['POST'])
def add_data():
    if request.form.get('key') not in API_KEYS:
        abort(403, description='FORBBIDEN.')
    else:
        try:
            app.logger.info(request.form.get('title'))
            alert = request.form.get('message')
            img = request.files['img']
            new_id = uuid.uuid4()

            filename = f"{new_id}.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(image_path)

            conn =  connect_db()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            # Insertar datos en la base de datos
            cur.execute("insert into camera_data (time, id, alert, seen) VALUES (NOW(), %s, %s, FALSE);", (str(new_id), alert))

            conn.commit()
            conn.close()

            return jsonify({'message': 'OK'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/data', methods=['GET'])
def get_data():
    
    query = """
        SELECT * FROM camera_data where seen=false
    """
    data = simple_querry(query)
    
    return jsonify(data)

@app.route('/data/all', methods=['GET'])
def get_latest_data():
    
    query = """
        SELECT * FROM camera_data
    """
    data = simple_querry(query)
    
    return jsonify(data)

@app.route('/see/<id>', methods=['GET'])
def seen(id):
    
    conn =  connect_db()
    cur = conn.cursor()

    app.logger.info(f'Seen img -> {id}')

    # Insertar datos en la base de datos
    cur.execute("UPDATE camera_data SET seen=TRUE WHERE id = %s;", (id,))

    conn.commit()
    conn.close()
    
    return render_template('seeImg.html', img=f'{id}.jpg')

@app.route('/img/<id>', methods=['GET'])
def send_image(id):
    
    filename = f'{id}.jpg'
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.logger.info('Starting server ...')
    app.run(host='0.0.0.0', port=5000, debug=True)
