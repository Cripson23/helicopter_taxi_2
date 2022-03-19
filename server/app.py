from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
import pymssql
import json
import datetime
from flask import request
import os
import pypandoc
from io import BytesIO
from docxtpl import DocxTemplate

app = Flask(__name__)
cors = CORS(app)
FORMS_FOLDER = os.path.join(app.root_path, "forms")

app.config['CORS_HEADERS'] = 'Content-Type'

conn = pymssql.connect(host='localhost', port='1433', server='DESKTOP-GNB4N0K', user='DESKTOP-GNB4N0K\sampt', password='Opel987654', database='helicoptertaxi')

print(conn)

# вовзвращает список шаблонов
@app.route('/api/forms')
@cross_origin()
def forms():
    form_list = []
    for f in os.listdir(FORMS_FOLDER):
        if f.endswith('.docx'):
            form_list.append(f)

    return jsonify({
        'forms': form_list
    })


# вовзвращает содержимое шаблона в html формате
@app.route("/api/form/<name>", methods = ['GET'])
@cross_origin()
def form(name):
    # вообще так делать не рекомендуется,
    # будет лучше если доступ к шаблонам будет осуществлятся по идентификатору
    # но для примера пойдет

    filename = os.path.join(FORMS_FOLDER, name)

    # сконвертируем файл с помощью pandoc
    output = pypandoc.convert_file(filename, "html")

    return jsonify({
        "html": output
    })


@app.route("/api/form/print/<name>")
def print_form(name):
    filename = os.path.join(FORMS_FOLDER, name)

    # открываем шаблон
    doc = DocxTemplate(filename)
    # передаем параметры запроса как значени плейсхолеров для шаблона
    doc.render(request.args.to_dict())

    # сохраняем результат заполнения docx в память
    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)

    # возвращаем файл
    return send_file(stream, mimetype='docx')


@app.route('/userAuth', methods = ['POST'])
@cross_origin()
def userAuth():
    request_data = request.get_json()
    userCode = request_data['userCode']
    inputPassword = request_data['inputPassword']
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Users WHERE userCode = '{userCode}' AND userPassword = '{inputPassword}'")
    row = cursor.fetchone()
    
    cursor.close()

    if row:
        return json.dumps({
            "auth": "success"
        })
    else:
        return json.dumps({
            "auth": "invalidPassword"
        })


@app.route('/employees', methods = ['GET'])
@cross_origin()
def getEmployees():

    employees = []
    content = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM СОТРУДНИК")
    row = cursor.fetchall()
    
    cursor.close()

    if row:
        for r in row:
            content = {'id': r[0], 'surname': r[1], 'name': r[2], 'patronymic': r[3], 'date_test_end': json_serial(r[4]), 'date_employment': json_serial(r[5]), 'branch_id': r[6]}
            employees.append(content)
        return json.dumps(employees)
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/dispetchers', methods = ['GET'])
@cross_origin()
def getDispetchers():

    dispetchers = []
    content = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM ДИСПЕТЧЕР")
    row = cursor.fetchall()

    cursor.close()

    if row:
        for r in row:
            content = {'id': r[0]}
            dispetchers.append(content)
        return json.dumps(dispetchers)
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/dispetchers/<int:id>', methods=["POST", "DELETE"])
@cross_origin()
def dispetchers(id):
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute(f"SET IDENTITY_INSERT ДИСПЕТЧЕР ON")
        cursor.execute(f"INSERT INTO ДИСПЕТЧЕР ([Код сотрудника]) VALUES ({id})")
        cursor.execute(f"SET IDENTITY_INSERT ДИСПЕТЧЕР OFF")
        conn.commit()

        return json.dumps({
            "answer": "success add dispetcher"
        })

    elif request.method == "DELETE":
        cursor.execute(f"DELETE FROM ДИСПЕТЧЕР WHERE [Код сотрудника] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete dispetcher"
        })

    cursor.close()

@app.route('/pilots', methods = ['GET'])
@cross_origin()
def getPilots():

    pilots = []
    content = {}
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ПИЛОТ")
    row = cursor.fetchall()

    cursor.close()

    if row:
        for r in row:
            content = {'id': r[0], 'license_renewal_date': json_serial(r[1])}
            pilots.append(content)
        return json.dumps(pilots)
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/pilots/<int:id>', methods=["POST", "DELETE"])
@cross_origin()
def pilots(id):
    cursor = conn.cursor()

    if request.method == "POST":
        request_data = request.get_json()
        license_renewal_date = request_data['license_renewal_date']

        cursor.execute(f"SET IDENTITY_INSERT ПИЛОТ ON")
        cursor.execute(f"INSERT INTO ПИЛОТ ([Код сотрудника], [Дата продления лицензии]) VALUES ({id}, '{license_renewal_date}')")
        cursor.execute(f"SET IDENTITY_INSERT ПИЛОТ OFF")
        conn.commit()

        return json.dumps({
            "answer": "success add pilot"
        })

    elif request.method == "DELETE":
        cursor.execute(f"DELETE FROM ПИЛОТ WHERE [Код сотрудника] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete pilot"
        })

    cursor.close()


@app.route('/addEmployee', methods = ['POST'])
@cross_origin()
def addEmployee():
    request_data = request.get_json()
    surname = request_data['surname']
    name = request_data['name']
    patronymic = request_data['patronymic']
    date_test_end = request_data['date_test_end']
    date_employment = request_data['date_employment']
    branch_id = request_data['branch_id']
    
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO СОТРУДНИК (Фамилия, Имя, Отчество, [Дата окончания исп срока], [Дата трудоустройства], [Код филиала]) VALUES ('{surname}', '{name}', '{patronymic}', '{date_test_end}', '{date_employment}', {branch_id})")
    conn.commit()

    cursor.close()

    return json.dumps({
        "answer": "success add employee"
    })


@app.route('/branchOptions', methods = ['GET'])
@cross_origin()
def getBranchOptions():

    branchOptions = []
    content = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT [Код филиала], Наименование FROM ФИЛИАЛ")
    row = cursor.fetchall()

    cursor.close()

    if row:
        for r in row:
            content = {'value': r[0], 'text': r[1]}
            branchOptions.append(content)
        return json.dumps(branchOptions)
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/employees/<int:id>', methods = ['DELETE', 'PUT'])
@cross_origin()
def employee(id):
    cursor = conn.cursor()

    if request.method == 'DELETE':
        cursor.execute(f"DELETE FROM СОТРУДНИК WHERE [Код сотрудника] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success delete employee"
        })
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        surname = request_data['surname']
        name = request_data['name']
        patronymic = request_data['patronymic']

        date_test_end = request_data['date_test_end']
        if date_test_end == '' or date_test_end == None:
            date_test_end_str = "[Дата окончания исп срока] = NULL"
        else:
            date_test_end_str = f"[Дата окончания исп срока] = '{date_test_end}'"
        date_employment = request_data['date_employment']

        branch_id = request_data['branch_id']

        cursor.execute(f"UPDATE СОТРУДНИК SET Фамилия = '{surname}', Имя = '{name}', Отчество = '{patronymic}',\
            {date_test_end_str}, [Дата трудоустройства] = '{date_employment}',\
            [Код филиала] = {branch_id} WHERE [Код сотрудника] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update employee"
        })

    cursor.close()


@app.route('/recertifications', methods = ['GET', 'POST', 'PUT'])
@cross_origin()
def recertifications():
    if request.method == 'GET':
        recerts = []
        content = {}
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM ПЕРЕАТТЕСТАЦИЯ")
        recerts_rows = cursor.fetchall()

        cursor.close()

        if recerts_rows:
            for r in recerts_rows:
                content = {'pilot_id': r[1], 'recert_date': json_serial(r[0])}

                cursor = conn.cursor()
                cursor.execute(f"SELECT Фамилия, Имя, Отчество FROM СОТРУДНИК WHERE [Код сотрудника] = {r[1]}")
                pilot_info_row = cursor.fetchall()
                
                for row in pilot_info_row:
                    content['surname'] = row[0]
                    content['name'] = row[1]
                    content['patronymic'] = row[2]

                cursor.close()

                recerts.append(content)

            return json.dumps(recerts)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    elif request.method == 'POST':
        cursor = conn.cursor()

        request_data = request.get_json()
        id = request_data['pilot_id']
        recert_date = request_data['recert_date']

        cursor.execute(f"INSERT INTO ПЕРЕАТТЕСТАЦИЯ ([Дата аттестации], [Код пилота]) VALUES ('{recert_date}', {id})")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add recert"
        })
    elif request.method == 'PUT':
        cursor = conn.cursor()

        request_data = request.get_json()

        last_pilot_id = request_data['last_pilot_id']
        last_recert_date = request_data['last_recert_date']
        id = request_data['pilot_id']
        recert_date = request_data['recert_date']

        cursor.execute(f"UPDATE ПЕРЕАТТЕСТАЦИЯ SET [Дата аттестации] = '{recert_date}', [Код пилота] = '{id}' WHERE [Дата аттестации] = '{last_recert_date}' AND [Код пилота] = {last_pilot_id}")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success update recert"
        })


@app.route('/recertifications/date/<int:id>', methods = ['GET'])
@cross_origin()
def getRecertDate(id):

    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 DATEADD(\"yyyy\",+2,[Дата аттестации]) AS [Дата переаттестации] FROM Переаттестация, СОТРУДНИК WHERE Переаттестация.[Код пилота]=[СОТРУДНИК].[Код сотрудника] And [СОТРУДНИК].[Код сотрудника]={id} ORDER BY [Дата аттестации] DESC;")
    rows = cursor.fetchall()

    cursor.close()

    if rows:
        for r in rows:
            return json.dumps({'date': json_serial(r[0])})
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/getPilots', methods = ['GET'])
@cross_origin()
def getFullPilots():

    recerts = []
    content = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT [Код сотрудника] FROM ПИЛОТ")
    recerts_rows = cursor.fetchall()

    cursor.close()

    if recerts_rows:
        for r in recerts_rows:
            content = {'id': r[0]}

            cursor = conn.cursor()
            cursor.execute(f"SELECT Фамилия, Имя, Отчество FROM СОТРУДНИК WHERE [Код сотрудника] = {r[0]}")
            pilot_info_row = cursor.fetchall()
            
            for row in pilot_info_row:
                content['surname'] = row[0]
                content['name'] = row[1]
                content['patronymic'] = row[2]

            cursor.close()

            recerts.append(content)

        return json.dumps(recerts)
    else:
        return json.dumps({
            "answer": "invalidResponse"
        })


@app.route('/deleteRecert', methods = ['POST'])
@cross_origin()
def deleteRecert():
    cursor = conn.cursor()

    request_data = request.get_json()

    id = request_data['id']
    recert_date = request_data['recert_date']

    cursor.execute(f"DELETE FROM ПЕРЕАТТЕСТАЦИЯ WHERE [Код пилота] = {id} AND [Дата аттестации] = '{recert_date}'")
    conn.commit()

    cursor.close()

    return json.dumps({
        "answer": "success delete recert"
    })


@app.route('/clients', methods = ['GET', 'POST'])
@cross_origin()
def clients():
    if request.method == 'GET':
        clients = []
        content = {}
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM КЛИЕНТ")
        row = cursor.fetchall()
        
        cursor.close()

        if row:
            for r in row:
                content = {'client_id': r[0], 'name': r[1], 'patronymic': r[2], 'phone_number': r[3], 'email': r[4]}
                clients.append(content)
            return json.dumps(clients)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    elif request.method == 'POST':
        request_data = request.get_json()

        name = request_data['name']
        patronymic = request_data['patronymic']
        phone_number = request_data['phone_number']
        email = request_data['email']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO КЛИЕНТ (Имя, Отчество, [Номер телефона], [Электронная почта]) VALUES ('{name}', '{patronymic}', '{phone_number}', '{email}')")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add client"
        })



@app.route('/clients/<int:id>', methods = ['DELETE', 'PUT'])
@cross_origin()
def client(id):
    cursor = conn.cursor()

    if request.method == 'DELETE':
        cursor.execute(f"DELETE FROM КЛИЕНТ WHERE [Код клиента] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success delete client"
        })
    
    elif request.method == 'PUT':
        request_data = request.get_json()

        name = request_data['name']
        patronymic = request_data['patronymic']
        phone_number = request_data['phone_number']
        email = request_data['email']

        cursor.execute(f"UPDATE КЛИЕНТ SET Имя = '{name}', Отчество = '{patronymic}', [Номер телефона] = '{phone_number}', [Электронная почта] = '{email}' WHERE [Код клиента] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update client"
        })

    cursor.close()


@app.route('/helicopters', methods = ['GET', 'POST'])
@cross_origin()
def getHelicopters():

    cursor = conn.cursor()
    if request.method == 'GET':
        helicopters = []
        content = {}
        cursor.execute("SELECT * FROM ВЕРТОЛЕТ")
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'model_id': r[1], 'year_issue': r[2], 'date_inspection': json_serial(r[3]), 'branch_id': r[4]}
                helicopters.append(content)
            return json.dumps(helicopters)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    elif request.method == 'POST':
        request_data = request.get_json()

        model_id = request_data['model_id']
        year_issue = request_data['year_issue']
        date_inspection = request_data['date_inspection']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO ВЕРТОЛЕТ ([Код модели], [Год выпуска], [Дата последнего тех осмотра], [Код филиала]) \
        VALUES ({model_id}, {year_issue}, '{date_inspection}', {branch_id})")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add helicopter"
        })
    
    cursor.close()


@app.route('/helicopters/<int:id>', methods=["DELETE", "PUT"])
@cross_origin()
def helicopters_del_put(id):
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute(f"DELETE FROM ВЕРТОЛЕТ WHERE [Код вертолета] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete helicopter"
        })
    
    elif request.method == "PUT":
        request_data = request.get_json()

        model_id = request_data['model_id']
        year_issue = request_data['year_issue']
        date_inspection = request_data['date_inspection']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"UPDATE ВЕРТОЛЕТ SET [Код модели] = {model_id}, [Год выпуска] = {year_issue}, [Дата последнего тех осмотра] = '{date_inspection}', [Код филиала] = {branch_id} WHERE [Код вертолета] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update helicopter"
        })
    
    cursor.close()


@app.route('/deleteRecyclingHelicopters', methods=["DELETE"])
@cross_origin()
def helicopters_del_recycling():
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ВЕРТОЛЕТ WHERE [Год выпуска]+20<=Year(CONVERT(date, GETDATE()))")
    conn.commit()

    return json.dumps({
        "answer": "success delete recycling helicopters"
    })


@app.route('/orders', methods = ['GET', 'POST'])
@cross_origin()
def getOrders():
    cursor = conn.cursor()

    if request.method == 'GET':
        orders = []
        content = {}
        
        cursor.execute("SELECT * FROM ЗАКАЗ")
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'dispetcher_id': r[1], 'pilot_id': r[2], 'client_id': r[3], 
                    'helicopter_id': r[4], 'order_address': r[5], 'delivery_address': r[6], 'date_completion': json_serial(r[7]),
                    'date_receipt': json_serial(r[8]), 'rental_time': r[9], 'payment_method': r[10], 'branch_id': r[11]}
                orders.append(content)
            return json.dumps(orders)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })

    elif request.method == 'POST':
        request_data = request.get_json()

        dispetcher_id = request_data['dispetcher_id']
        pilot_id = request_data['pilot_id']
        client_id = request_data['client_id']
        helicopter_id = request_data['helicopter_id']
        order_address = request_data['order_address']
        delivery_address = request_data['delivery_address']
        date_completion = request_data['date_completion']
        date_receipt = request_data['date_receipt']
        rental_time = request_data['rental_time']
        payment_method = request_data['payment_method']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO ЗАКАЗ ([Код диспетчера], [Код пилота], [Код клиента], [Код вертолета], [Адрес заказа], [Адрес доставки], [Дата выполнения заказа], [Дата поступления заказа], [Время аренды], [Способ оплаты], [Код филиала]) \
        VALUES ('{dispetcher_id}', '{pilot_id}', '{client_id}', '{helicopter_id}', '{order_address}', '{delivery_address}', '{date_completion}', '{date_receipt}', '{rental_time}', '{payment_method}', '{branch_id}')")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add order"
        })


@app.route('/helicopter-models', methods = ['GET', 'POST'])
@cross_origin()
def helicopter_model():
    cursor = conn.cursor()
    models = []

    if request.method == 'GET':
        cursor.execute(f"SELECT [Код модели], [Наименование модели], Вместимость, Скорость, Дальность, [Стоимость одного часа аренды] FROM [МОДЕЛЬ ВЕРТОЛЕТА]")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'name': r[1], 'capacity': r[2], 'speed': r[3], 'range': r[4], 'price': r[5]}
                models.append(content)

            return json.dumps(models)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    elif request.method == 'POST':
        request_data = request.get_json()

        name = request_data['name']
        capacity = request_data['capacity']
        speed = request_data['speed']
        range = request_data['range']
        price = request_data['price']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO [МОДЕЛЬ ВЕРТОЛЕТА] ([Наименование модели], Вместимость, Скорость, Дальность, [Стоимость одного часа аренды]) VALUES ('{name}', {capacity}, {speed}, {range}, {price})")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add helicopter model"
        })


@app.route('/helicopter-models/<int:id>', methods=["DELETE", "PUT"])
@cross_origin()
def models_del_put(id):
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute(f"DELETE FROM [МОДЕЛЬ ВЕРТОЛЕТА] WHERE [Код модели] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete helicopter model"
        })
    
    elif request.method == "PUT":
        request_data = request.get_json()

        name = request_data['name']
        capacity = request_data['capacity']
        speed = request_data['speed']
        range = request_data['range']
        price = request_data['price']

        cursor = conn.cursor()

        cursor.execute(f"UPDATE [МОДЕЛЬ ВЕРТОЛЕТА] SET [Наименование модели] = '{name}', Вместимость = {capacity}, Скорость = {speed}, Дальность = {range}, [Стоимость одного часа аренды] = {price} WHERE [Код модели] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update helicopter model"
        })
    
    cursor.close()


@app.route('/orders/<int:id>', methods=["DELETE", "PUT"])
@cross_origin()
def orders(id):
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute(f"DELETE FROM ЗАКАЗ WHERE [Код заказа] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete order"
        })
    
    elif request.method == "PUT":
        request_data = request.get_json()

        dispetcher_id = request_data['dispetcher_id']
        pilot_id = request_data['pilot_id']
        client_id = request_data['client_id']
        helicopter_id = request_data['helicopter_id']
        order_address = request_data['order_address']
        delivery_address = request_data['delivery_address']
        date_completion = request_data['date_completion']
        date_receipt = request_data['date_receipt']
        rental_time = request_data['rental_time']
        payment_method = request_data['payment_method']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"UPDATE ЗАКАЗ SET [Код диспетчера] = {dispetcher_id}, [Код пилота] = {pilot_id}, [Код клиента] = {client_id}, \
            [Код вертолета] = {helicopter_id}, [Адрес заказа] = '{order_address}', [Адрес доставки] = '{delivery_address}', [Дата выполнения заказа] = '{date_completion}', \
            [Дата поступления заказа] = '{date_receipt}', [Время аренды] = {rental_time}, [Способ оплаты] = '{payment_method}', [Код филиала] = {branch_id} WHERE [Код заказа] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update order"
        })
    
    cursor.close()


@app.route('/providers', methods = ['GET', 'POST'])
@cross_origin()
def providers():
    cursor = conn.cursor()

    if request.method == 'GET':
        providers = []
        content = {}
        
        cursor.execute("SELECT * FROM [ПОСТАВЩИК ТОПЛИВА]")
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'name': r[1], 'address': r[2], 'phone_number': r[3], 
                    'fio_director': r[4], 'branch_id': r[5]}
                providers.append(content)
            return json.dumps(providers)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    
    elif request.method == 'POST':
        request_data = request.get_json()

        name = request_data['name']
        address = request_data['address']
        phone_number = request_data['phone_number']
        fio_director = request_data['fio_director']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO [ПОСТАВЩИК ТОПЛИВА] ([Наименование поставщика], [Адрес поставщика],\
            [Телефон поставщика], [ФИО директора], [Код филиала]) VALUES ('{name}', '{address}', '{phone_number}', '{fio_director}', {branch_id})")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add provider"
        })


@app.route('/providers/<int:id>', methods=["DELETE", "PUT"])
@cross_origin()
def providers_del_put(id):
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute(f"DELETE FROM [ПОСТАВЩИК ТОПЛИВА] WHERE [Код поставщика] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete provider"
        })
    
    elif request.method == "PUT":
        request_data = request.get_json()

        name = request_data['name']
        address = request_data['address']
        phone_number = request_data['phone_number']
        fio_director = request_data['fio_director']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"UPDATE [ПОСТАВЩИК ТОПЛИВА] SET [Наименование поставщика] = '{name}', [Адрес поставщика] = '{address}', [Телефон поставщика] = '{phone_number}', \
            [ФИО директора] = '{fio_director}', [Код филиала] = {branch_id} WHERE [Код поставщика] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update provider"
        })
    
    cursor.close()


@app.route('/purchases', methods = ['GET', 'POST'])
@cross_origin()
def purchases():
    cursor = conn.cursor()

    if request.method == 'GET':
        purchases = []
        content = {}
        
        cursor.execute("SELECT * FROM [ЗАКУПКА ТОПЛИВА]")
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'provider_id': r[1], 'volume': r[2], 'date': json_serial(r[3]), 'price': r[4], 'branch_id': r[5]}
                purchases.append(content)
            return json.dumps(purchases)
        else:
            return json.dumps({
                "answer": "invalidResponse"
            })
    
    elif request.method == 'POST':
        request_data = request.get_json()

        provider_id = request_data['provider_id']
        volume = request_data['volume']
        date = request_data['date']
        price = request_data['price']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO [ЗАКУПКА ТОПЛИВА] ([Код поставщика], [Объем закупки],\
            [Дата закупки], [Стоимость топлива (за 1л)], [Код филиала]) VALUES ({provider_id}, {volume}, '{date}', {price}, {branch_id})")
        conn.commit()

        cursor.close()
        return json.dumps({
            "answer": "success add purchase"
        })


@app.route('/purchases/<int:id>', methods=["DELETE", "PUT"])
@cross_origin()
def purchases_del_put(id):
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute(f"DELETE FROM [ЗАКУПКА ТОПЛИВА] WHERE [Код закупки] = {id}")
        conn.commit()

        return json.dumps({
            "answer": "success delete purchase"
        })
    
    elif request.method == "PUT":
        request_data = request.get_json()

        provider_id = request_data['provider_id']
        volume = request_data['volume']
        date = request_data['date']
        price = request_data['price']
        branch_id = request_data['branch_id']

        cursor = conn.cursor()

        cursor.execute(f"UPDATE [ЗАКУПКА ТОПЛИВА] SET [Код поставщика] = '{provider_id}', [Объем закупки] = '{volume}', [Дата закупки] = '{date}', \
            [Стоимость топлива (за 1л)] = '{price}', [Код филиала] = {branch_id} WHERE [Код закупки] = {id}")
        conn.commit()
        return json.dumps({
            "answer": "success update purchase"
        })
    
    cursor.close()


@app.route('/providers/most-profitable', methods = ['POST'])
@cross_origin()
def providers_profitable():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        providers = []
        content = {}
        
        cursor.execute(f"SELECT [Наименование поставщика], [ПОСТАВЩИК ТОПЛИВА].[Код поставщика],\
            Count([ЗАКУПКА ТОПЛИВА].[Код поставщика]) AS [Кол-во закупок],\
            Sum([ЗАКУПКА ТОПЛИВА].[Объем закупки]) AS [Общий объем закупок],\
            round(CONVERT(float, Sum([ЗАКУПКА ТОПЛИВА].[Стоимость топлива (за 1л)]))/CONVERT(float, Sum([ЗАКУПКА ТОПЛИВА].[Объем закупки])), 2) AS [Средняя цена за 1л]\
            FROM [dbo].[ПОСТАВЩИК ТОПЛИВА], [dbo].[ЗАКУПКА ТОПЛИВА]\
            WHERE [ПОСТАВЩИК ТОПЛИВА].[Код поставщика]=[ЗАКУПКА ТОПЛИВА].[Код поставщика] AND (([ЗАКУПКА ТОПЛИВА].[Дата закупки] >= CONVERT(datetime, '{date_start}')) AND ([ЗАКУПКА ТОПЛИВА].[Дата закупки] <= CONVERT(datetime, '{date_end}')))\
            GROUP BY [ПОСТАВЩИК ТОПЛИВА].[Наименование поставщика], [ПОСТАВЩИК ТОПЛИВА].[Код поставщика] ORDER BY [Средняя цена за 1л];")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'name': r[0], 'id': r[1], 'purchase_count': r[2], 'volume_count': r[3], 'avg_price': r[4]}
                providers.append(content)
            return json.dumps(providers)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/clients/most-active', methods = ['POST'])
@cross_origin()
def clients_active():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        clients = []
        content = {}
        
        cursor.execute(f"SELECT TOP 3 КЛИЕНТ.[Код клиента], КЛИЕНТ.Имя, КЛИЕНТ.[Номер телефона], COUNT(*) as [Количество заказов] FROM КЛИЕНТ, ЗАКАЗ\
        WHERE КЛИЕНТ.[Код клиента] = ЗАКАЗ.[Код клиента] and ЗАКАЗ.[Дата поступления заказа] >= '{date_start}' and ЗАКАЗ.[Дата поступления заказа] <= '{date_end}' GROUP BY КЛИЕНТ.[Код клиента], КЛИЕНТ.Имя, КЛИЕНТ.[Номер телефона]\
        ORDER BY [Количество заказов] DESC")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'name': r[1], 'phone_number': r[2], 'orders_count': r[3]}
                clients.append(content)
            return json.dumps(clients)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/pilots/most-active', methods = ['POST'])
@cross_origin()
def pilots_active():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        pilots = []
        content = {}
        
        cursor.execute(f"SELECT TOP 3 ПИЛОТ.[Код сотрудника], СОТРУДНИК.Фамилия, СОТРУДНИК.Имя, COUNT(*) as [Количество заказов] FROM СОТРУДНИК, ПИЛОТ, ЗАКАЗ\
            WHERE ПИЛОТ.[Код сотрудника] = СОТРУДНИК.[Код сотрудника] AND ЗАКАЗ.[Код пилота] = ПИЛОТ.[Код сотрудника] AND ЗАКАЗ.[Дата поступления заказа] >= '{date_start}' AND ЗАКАЗ.[Дата поступления заказа] <= '{date_end}'\
            GROUP BY СОТРУДНИК.Фамилия, СОТРУДНИК.Имя, ПИЛОТ.[Код сотрудника] ORDER BY [Количество заказов] DESC")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'surname': r[1], 'name': r[2], 'orders_count': r[3]}
                pilots.append(content)
            return json.dumps(pilots)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/dispetchers/most-active', methods = ['POST'])
@cross_origin()
def dispetchers_active():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        dispetchers = []
        content = {}
        
        cursor.execute(f"SELECT TOP 3 ДИСПЕТЧЕР.[Код сотрудника], СОТРУДНИК.Фамилия, СОТРУДНИК.Имя, COUNT(*) as [Количество заказов] FROM СОТРУДНИК, ДИСПЕТЧЕР, ЗАКАЗ\
            WHERE ДИСПЕТЧЕР.[Код сотрудника] = СОТРУДНИК.[Код сотрудника] AND ЗАКАЗ.[Код диспетчера] = ДИСПЕТЧЕР.[Код сотрудника] AND ЗАКАЗ.[Дата поступления заказа] >= '{date_start}' AND ЗАКАЗ.[Дата поступления заказа] <= '{date_end}'\
            GROUP BY СОТРУДНИК.Фамилия, СОТРУДНИК.Имя, ДИСПЕТЧЕР.[Код сотрудника] ORDER BY [Количество заказов] DESC")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'surname': r[1], 'name': r[2], 'orders_count': r[3]}
                dispetchers.append(content)
            return json.dumps(dispetchers)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/dispetchers/count-orders', methods = ['POST'])
@cross_origin()
def dispetchers_count_orders():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        dispetchers = []
        content = {}
        
        cursor.execute(f"SELECT [ДИСПЕТЧЕР].[Код сотрудника], [СОТРУДНИК].Фамилия, [СОТРУДНИК].Имя, COUNT([ЗАКАЗ].[Код диспетчера]) AS [Кол-во] FROM ДИСПЕТЧЕР, ЗАКАЗ, СОТРУДНИК WHERE ([ДИСПЕТЧЕР].[Код сотрудника]=[ЗАКАЗ].[Код диспетчера] And [ДИСПЕТЧЕР].[Код сотрудника] = [СОТРУДНИК].[Код сотрудника])\
                And ([ЗАКАЗ].[Дата выполнения заказа]>='{date_start}'\
                And [ЗАКАЗ].[Дата выполнения заказа]<='{date_end}')\
            GROUP BY [ДИСПЕТЧЕР].[Код сотрудника], [СОТРУДНИК].Фамилия, [СОТРУДНИК].Имя;")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'surname': r[1], 'name': r[2], 'orders_count': r[3]}
                dispetchers.append(content)
            return json.dumps(dispetchers)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/pilots/count-orders', methods = ['POST'])
@cross_origin()
def pilots_count_orders():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        pilots = []
        content = {}
        
        cursor.execute(f"SELECT [ПИЛОТ].[Код сотрудника], [СОТРУДНИК].Фамилия, [СОТРУДНИК].Имя, COUNT([ЗАКАЗ].[Код пилота]) AS [Кол-во перелётов]\
            FROM ПИЛОТ, СОТРУДНИК, ЗАКАЗ\
            WHERE ([ПИЛОТ].[Код сотрудника]=[ЗАКАЗ].[Код пилота] And [ПИЛОТ].[Код сотрудника] = [СОТРУДНИК].[Код сотрудника])\
                And ([ЗАКАЗ].[Дата выполнения заказа]>='{date_start}'\
                And [ЗАКАЗ].[Дата выполнения заказа]<='{date_end}')\
            GROUP BY [ПИЛОТ].[Код сотрудника], [СОТРУДНИК].Фамилия, [СОТРУДНИК].Имя;")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'surname': r[1], 'name': r[2], 'orders_count': r[3]}
                pilots.append(content)
            return json.dumps(pilots)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/helicopters/count-orders', methods = ['POST'])
@cross_origin()
def helicopters_count_orders():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        helicopters = []
        content = {}
        
        cursor.execute(f"SELECT [ВЕРТОЛЕТ].[Код вертолета], [МОДЕЛЬ ВЕРТОЛЕТА].[Наименование модели],\
            COUNT([ЗАКАЗ].[Код вертолета]) AS [Кол-во заказов]\
            FROM ВЕРТОЛЕТ, [МОДЕЛЬ ВЕРТОЛЕТА], ЗАКАЗ\
            WHERE [ВЕРТОЛЕТ].[Код вертолета]=[ЗАКАЗ].[Код вертолета]\
                And [ВЕРТОЛЕТ].[Код модели]=[МОДЕЛЬ ВЕРТОЛЕТА].[Код модели]\
                And [ЗАКАЗ].[Дата выполнения заказа]>='{date_start}'\
                And [ЗАКАЗ].[Дата выполнения заказа]<='{date_end}'\
            GROUP BY [ВЕРТОЛЕТ].[Код вертолета], [МОДЕЛЬ ВЕРТОЛЕТА].[Наименование модели];")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                content = {'id': r[0], 'model_name': r[1], 'orders_count': r[2]}
                helicopters.append(content)
            return json.dumps(helicopters)
        else:
            return json.dumps({
                "answer": "Not founded"
            })


@app.route('/purchases/cost', methods = ['POST'])
@cross_origin()
def purchases_cost():
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        date_start = request_data['date_start']
        date_end = request_data['date_end']

        purchases = []
        content = {}
        
        cursor.execute(f"SELECT SUM([ЗАКУПКА ТОПЛИВА].[Стоимость топлива (за 1л)] * [ЗАКУПКА ТОПЛИВА].[Объем закупки]) AS [Общие затраты], SUM([ЗАКУПКА ТОПЛИВА].[Объем закупки]) AS [Общий объём]\
                        FROM [ЗАКУПКА ТОПЛИВА]\
                        WHERE [ЗАКУПКА ТОПЛИВА].[Дата закупки] >= '{date_start}' And [ЗАКУПКА ТОПЛИВА].[Дата закупки]<='{date_end}';")
        
        row = cursor.fetchall()

        cursor.close()

        if row:
            for r in row:
                if r[0] != None and r[1] != None:
                    content = {'cost': r[0], 'volume': r[1]}
                    purchases.append(content)
                    return json.dumps(purchases)
                else:
                    return json.dumps({
                        "answer": "Not founded"
                    })


@app.route('/my-orders/<userType>', methods = ['POST'])
@cross_origin()
def get_my_orders(userType):
    cursor = conn.cursor()

    if request.method == 'POST':
        request_data = request.get_json()

        surname = request_data['surname']
        name = request_data['name']
        employee_id = None
        employee_info = None

        cursor.execute(f"SELECT [Код сотрудника], Фамилия, Имя FROM СОТРУДНИК WHERE Фамилия = '{surname}' AND Имя = '{name}'")
        row = cursor.fetchall()

        if row:
            for r in row:
                employee_info = "ID: " + str(r[0]) + " | " + r[1] + " " + r[2]
                employee_id = r[0]
        
        if employee_id == None:
            return json.dumps({'answer': 'Not founded'})

        if userType == 'dispetcher':
            cursor.execute(f"SELECT [Код заказа], [Код пилота], [Код клиента], [Код вертолета], [Адрес заказа], [Адрес доставки], [Дата выполнения заказа], [Дата поступления заказа],\
                        [Время аренды], [Способ оплаты], [Код филиала] FROM ЗАКАЗ WHERE [Код диспетчера] = {employee_id}")
        elif userType == 'pilot':
            cursor.execute(f"SELECT [Код заказа], [Код диспетчера], [Код клиента], [Код вертолета], [Адрес заказа], [Адрес доставки], [Дата выполнения заказа], [Дата поступления заказа],\
                        [Время аренды], [Способ оплаты], [Код филиала] FROM ЗАКАЗ WHERE [Код пилота] = {employee_id}")

        my_orders = []
        orders = cursor.fetchall()
        for order in orders:
            content = {}
            content['id'] = order[0]
            content['order_address'] = order[4]
            content['delivery_address'] = order[5]
            content['date_receipt'] = json_serial(order[6])
            content['date_completion'] = json_serial(order[7])
            content['rental_time'] = order[8]
            content['payment_method'] = order[9]
            content['branch_id'] = order[10]

            if userType == 'dispetcher':
                content['dispetcher'] = employee_info
            elif userType == 'pilot':
                content['pilot'] = employee_info

            cursor.execute(f"SELECT Фамилия, Имя FROM СОТРУДНИК WHERE [Код сотрудника] = {order[1]}")
            emoloyee = cursor.fetchall()

            for e in emoloyee:
                if userType == 'dispetcher':
                    content['pilot'] = "ID: " + str(order[1]) + " | " + e[0] + " " + e[1]

                elif userType == 'pilot':
                    content['dispetcher'] = "ID: " + str(order[1]) + " | " + e[0] + " " + e[1]

            cursor.execute(f"SELECT [Номер телефона] FROM КЛИЕНТ WHERE [Код клиента] = {order[2]}")
            clients = cursor.fetchall()
            for client in clients:
                content['client'] = client[0]

            cursor.execute(f"SELECT [Код модели] FROM ВЕРТОЛЕТ WHERE [Код вертолета] = {order[3]}")
            helicopters = cursor.fetchall()
            for helicopter in helicopters:
                cursor.execute(f"SELECT [Наименование модели] FROM [МОДЕЛЬ ВЕРТОЛЕТА] WHERE [Код модели] = {helicopter[0]}")
                models = cursor.fetchall()
                for model in models:
                    content['helicopter'] = "ID: " + str(order[3]) + " | " + model[0]
            
            my_orders.append(content)
        
        return json.dumps(my_orders)


@app.route('/my-recertification', methods = ['POST'])
@cross_origin()
def getMyRecertDate():
    request_data = request.get_json()

    surname = request_data['surname']
    name = request_data['name']

    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 DATEADD(\"yyyy\",+2,[Дата аттестации]) AS [Дата переаттестации] FROM Переаттестация, СОТРУДНИК WHERE Переаттестация.[Код пилота]=[СОТРУДНИК].[Код сотрудника] And [СОТРУДНИК].Фамилия='{surname}' AND [СОТРУДНИК].Имя='{name}' ORDER BY [Дата аттестации] DESC;")
    rows = cursor.fetchall()

    cursor.close()

    if rows:
        for r in rows:
            return json.dumps({'date': json_serial(r[0])})
    else:
        return json.dumps({
            "date": "Not found"
        })


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if obj is None:
        return obj
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))