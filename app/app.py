from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pymysql
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__, static_folder='..', static_url_path='/')
CORS(app)

# Global variable to hold the database connection
db_connection = None
db_type = None

def get_mongo_db(uri):
    """Establishes a connection to a MongoDB database."""
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return client.get_default_database()
    except ConnectionFailure:
        return None

def get_mysql_db(uri):
    """Establishes a connection to a MySQL database."""
    try:
        # pymysql URI format: mysql+pymysql://user:password@host/db
        # We need to parse this for pymysql.connect
        # Stripping 'mysql+pymysql://'
        uri_details = uri.replace('mysql+pymysql://', '')
        user_pass, host_db = uri_details.split('@')
        user, password = user_pass.split(':')
        host, db = host_db.split('/')

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/connect', methods=['POST'])
def connect_db():
    global db_connection, db_type
    data = request.json
    db_type = data.get('type')
    uri = data.get('uri')

    if not db_type or not uri:
        return jsonify({"status": "error", "message": "Missing database type or URI"}), 400

    if db_type == 'mongodb':
        db_connection = get_mongo_db(uri)
    elif db_type == 'mysql':
        db_connection = get_mysql_db(uri)
    else:
        return jsonify({"status": "error", "message": "Unsupported database type"}), 400

    if db_connection:
        # For MySQL, check if the connection is alive
        if db_type == 'mysql' and not db_connection.open:
             return jsonify({"status": "error", "message": "Connection failed"}), 500
        return jsonify({"status": "success", "message": "Database connected successfully"})
    else:
        return jsonify({"status": "error", "message": "Connection failed"}), 500

@app.route('/api/records', methods=['GET', 'POST'])
def handle_records():
    global db_connection, db_type

    if not db_connection:
        return jsonify({"status": "error", "message": "Database not connected"}), 500

    if request.method == 'POST':
        data = request.json
        company_name = data.get('company_name')
        industry = data.get('industry')
        notes = data.get('notes')

        if not company_name or not industry:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        try:
            if db_type == 'mongodb':
                db_connection.companies.insert_one({
                    "company_name": company_name,
                    "industry": industry,
                    "notes": notes
                })
            elif db_type == 'mysql':
                # Ensure table exists
                with db_connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS companies (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        company_name VARCHAR(255) NOT NULL,
                        industry VARCHAR(255) NOT NULL,
                        notes TEXT
                    )
                    """)
                    sql = "INSERT INTO companies (company_name, industry, notes) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (company_name, industry, notes))
                db_connection.commit()
            return jsonify({"status": "success", "message": "Record added"}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'GET':
        try:
            if db_type == 'mongodb':
                records = list(db_connection.companies.find({}, {'_id': 0}))
                return jsonify(records)
            elif db_type == 'mysql':
                with db_connection.cursor() as cursor:
                    # Check if table exists before querying
                    cursor.execute("SHOW TABLES LIKE 'companies'")
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("SELECT company_name, industry, notes FROM companies")
                        records = cursor.fetchall()
                        return jsonify(records)
                    else:
                        # If table doesn't exist, return empty list
                        return jsonify([])
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)