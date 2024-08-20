import pandas as pd
from flask import Flask, jsonify
from flask_restful import Resource, Api

# Cargar los datos desde los archivos CSV
df1 = pd.read_csv('API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', sep=',', engine='python', on_bad_lines='skip')
df2 = pd.read_csv('Metadata_Country_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', sep=',', engine='python', on_bad_lines='skip')
df3 = pd.read_csv('Metadata_Indicator_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', sep=',', engine='python', on_bad_lines='skip')  

# Crear la aplicación Flask y configurar Flask-RESTful
app = Flask(__name__)
api = Api(app)

# Definir los recursos para cada conjunto de datos
class Data1(Resource):
    def get(self):
        return jsonify(df1.to_dict(orient='records'))

class Data2(Resource):
    def get(self):
        return jsonify(df2.to_dict(orient='records'))

class Data3(Resource):
    def get(self):
        return jsonify(df3.to_dict(orient='records'))

# Registrar los recursos con sus respectivos endpoints
api.add_resource(Data1, '/api/v1/data1')
api.add_resource(Data2, '/api/v1/data2')
api.add_resource(Data3, '/api/v1/data3')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)


