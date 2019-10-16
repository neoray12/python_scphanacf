import os
from flask import Flask
from flask import request
from hdbcli import dbapi
from cfenv import AppEnv

app = Flask(__name__)
env = AppEnv()

hana = env.get_service(label='hana-db')
host= hana.credentials['host']
hanaport= hana.credentials['port']
haascert= hana.credentials['certificate']

@app.route("/")
def hello():

# local connection to SAP Cloud Platform Hana Service

    # conn = dbapi.connect(
    # address="<hana-db.servicekey.host>",
    # port=<hana-db.servicekey.port>,
	# encrypt="true",
    # user="<username>",
    # password="<password>"
    # )

# SAP Cloud Platform Cloud Foundry Connection to Hana Service

    conn = dbapi.connect(
        address=host,
        port=int(hanaport), 
        user="<username>",
        password="<password>",
        encrypt="true",
        sslValidateCertificate="true",
        sslCryptoProvider="openssl",
        sslTrustStore=haascert
        )

    with conn.cursor() as cursor:
	    sql = "select SYSTEM_ID, DATABASE_NAME, HOST, VERSION, USAGE from M_DATABASE"
	    cursor.execute(sql)
	    result = cursor.fetchall()
    resultInString = str(result).strip('[]')

    return "SAP Cloud Platform HANA Service Connected!" + resultInString

@app.route("/post", methods=['GET', 'POST'])
def submit():

# local connection to SAP Cloud Platform Hana Service

    # conn = dbapi.connect(
    #     address="zeus.hana.prod.ap-northeast-1.whitney.dbaas.ondemand.com",
    #     port=20185,
	#     encrypt="true",
    #     user="SYSTEM",
    #     password="#EDC2wsx"
    # )

# SAP Cloud Platform Cloud Foundry Connection to Hana Service

    conn = dbapi.connect(
        address=host,
        port=int(hanaport), 
        user="<username>",
        password="<password>",
        encrypt="true",
        sslValidateCertificate="true",
        sslCryptoProvider="openssl",
        sslTrustStore=haascert
        )
    
    if request.method == 'POST':

        parameter1 = request.values['parameter1']
        parameter2 = request.values['parameter2']
        parameter3 = request.values['parameter3']

    with conn.cursor() as cursor:   
        sql = "INSERT INTO \"SYSTEM\".\"PYTHONWEBSERVICE\" VALUES('"+parameter1+"','"+parameter2+"','"+parameter3+"');"
        cursor.execute(sql)

        return "成功將資料存入 HANA 資料庫 " + "Parameter1 = " + parameter1 + " Parameter2 = " + parameter2 + " Parameter3 = " + parameter3
    return "成功將資料存入 HANA 資料庫 " + "Parameter1 = " + parameter1 + " Parameter2 = " + parameter2 + " Parameter3 = " + parameter3

if __name__ == "__main__":
    osPort = os.getenv("PORT")
    if osPort == None:
        port = 5000
    else:
        port = int(osPort)
    app.run(host='0.0.0.0',port=port)





