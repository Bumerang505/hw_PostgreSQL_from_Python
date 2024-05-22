import psycopg2

conn = psycopg2.connect(database='netology_db', user='postgres', password='postgres')


def create_table_clients():
    with conn.cursor() as cur:
        cur.execute('''
                        CREATE TABLE IF NOT EXISTS Clients (
                            id   	   SERIAL PRIMARY KEY,
                            first_name VARCHAR(40) NOT NULL,
                            last_name  VARCHAR(40) NOT NULL,
                            email      VARCHAR(80) NOT NULL UNIQUE);
                        ''')
        conn.commit()


def create_table_phones():
    with conn.cursor() as cur:
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Phones (
                        phone_id  SERIAL PRIMARY KEY,
	                    phone     BIGINT,
	                    client_id INTEGER NOT NULL REFERENCES Clients(id));
	                ''')
        conn.commit()


def add_new_client(first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute('''
                        INSERT INTO Clients(first_name, last_name, email)
                        VALUES(%s, %s, %s);
                        ''', (first_name, last_name, email))
        conn.commit()

    with conn.cursor() as cur:
        cur.execute('''
                    SELECT id
                    FROM Clients
                    ORDER BY id DESC
                    LIMIT 1;
                    ''')
        client_id = cur.fetchone()[0]

    with conn.cursor() as cur:
        cur.execute('''
                        INSERT INTO phones(phone, client_id)
                        VALUES(%s, %s);
                        ''', (phone, client_id)
                    )
        conn.commit()


def add_phone_to_exists_client(phone, client_id):
    with conn.cursor() as cur:
        cur.execute(
            ''' 
            INSERT INTO phones(phone, client_id)
            VALUES(%s, %s);
            ''', (phone, client_id)
        )
        conn.commit()


def     change_clients_values(client_id, parameter, new_value):
    if parameter != 'phone':
        with conn.cursor() as cur:
            cur.execute(
                f'UPDATE Clients '
                f'SET {parameter} = %s '
                f'WHERE id = %s;'
                , (new_value, client_id)
            )
            conn.commit()
    else:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT phone
                FROM phones 
                WHERE client_id = %s;
                ''', (client_id,)
            )
            list_phones = cur.fetchall()
        if len(list_phones) > 1:
            many_phones_list = []
            for i in list_phones:
                many_phones_list.append(i[0])

            phone_for_change = int(input(f'У пользователя несколько телефонов {many_phones_list}. Введите номер, '
                                         f'который нужно изменить: '))
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE phones 
                    SET phone = %s
                    WHERE phone = %s;
                    ''', (new_value, phone_for_change)
                )
                conn.commit()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE phones 
                    SET phone = %s
                    WHERE client_id = %s;
                    ''', (new_value, client_id)
                )
                conn.commit()


def delete_clients_phone(phone_id):
    with conn.cursor() as cur:
        cur.execute(
            '''
            DELETE FROM phones
            WHERE phone_id = %s;
            ''', (phone_id,)
        )
        conn.commit()


def delete_client(client_id):
    with conn.cursor() as cur:
        cur.execute(
            '''
            DELETE FROM phones 
            WHERE  client_id = %s;
            ''', (client_id,)
        )
        conn.commit()

    with conn.cursor() as cur:
        cur.execute(
            '''
            DELETE FROM clients 
            WHERE  id = %s;
            ''', (client_id,)
        )
        conn.commit()


def find_client():
    parameter = input('Введите параметр, по которому будет осуществляться поиск (имя, фамилия, email, телефон) ')
    if parameter == 'имя':
        parameter = 'first_name'
    if parameter == 'фамилия':
        parameter = 'last_name'
    if parameter == 'телефон':
        parameter = 'phone'

    value_parameter = input('Укажите значение параметра: ')

    if parameter != 'phone':
        with conn.cursor() as cur:
            cur.execute(
                f'SELECT id '
                f'FROM Clients '
                f'WHERE {parameter} = %s'
                , (value_parameter,)
            )
            print(f'Client_id = {cur.fetchall()[0][0]}')
    else:
        with conn.cursor() as cur:
            cur.execute(
                f'SELECT Client_id '
                f'FROM Phones '
                f'WHERE {parameter} = %s'
                , (value_parameter,)
            )
            print(f'Client_id = {cur.fetchall()[0][0]}')


create_table_clients()
create_table_phones()
add_new_client('Adam', 'Sandler', 'adam@mail.ru', 89996665544)
add_phone_to_exists_client(88999998, 2)
change_clients_values(2, 'phone', 505606)
delete_clients_phone(1)
delete_client(1)
find_client()

conn.close()
