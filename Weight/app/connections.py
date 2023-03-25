import mysql.connector
from datetime import datetime, date
import check

def get_connection():
    db = mysql.connector.connect(
        host="weight-db",
        user="root",
        port=3306,
        password="123",
        database="weight"
    )

    return db

db = get_connection()
cursor = db.cursor()

def convert_lbs_to_kg(weight):
    return int(weight) * 0.45359237 

def get_transactions_by_date_range_for_truck(truck_id,start_date, end_date):
    sql = "SELECT * FROM transactions WHERE truck = %s AND datetime BETWEEN %s AND %s AND direction IN ('in','none')"
    input_data = (truck_id, start_date, end_date)
    cursor.execute(sql, input_data)
    results = cursor.fetchall()
    transactions = []
    for row in results:
        transaction = {
            'id': row[0],
            'datetime': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'direction': row[2],
            'truck': row[3],
            'bruto': row[4],
            'truckTara': row[5],
            'produce': row[6]
        }
        transactions.append(transaction)
    return transactions

def get_last_known_tara(truck_id,start_date, end_date):
    sql = "SELECT truckTara FROM transactions WHERE truck = %s AND datetime BETWEEN %s AND %s AND direction = 'out'"
    input_data = (truck_id,start_date, end_date,)
    cursor.execute(sql, input_data)
    results = cursor.fetchall()
    if len(results) == 0:
        return 'na'
    return results[-1][0]

def check_if_container_transaction_between_dates(transaction_id,start_date, end_date):
    sql = "SELECT * FROM transactions WHERE id = %s AND datetime BETWEEN %s AND %s"
    input_data = (transaction_id, start_date, end_date)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def get_transactions_by_date_range(start_date, end_date, direction):
    filter_list = direction.split(',')
    placeholder_str = ','.join(['%s'] * len(filter_list))
    sql = "SELECT * FROM transactions WHERE datetime BETWEEN %s AND %s AND direction IN ({})".format(placeholder_str)
    input_data = (start_date, end_date) + tuple(filter_list)
    cursor.execute(sql, input_data)
    results = cursor.fetchall()
    transactions = []
    for row in results:
        transaction = {
            'id': row[0],
            'datetime': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'direction': row[2],
            'truck': row[3],
            'bruto': row[4],
            'truckTara': row[5],
            'produce': row[6]
        }
        transactions.append(transaction)
    return transactions

def insert_transaction(direction, truck, bruto, produce, truckTara=None):
    # this function inserts a new transaction to transactions table
    # this function returns the id of the new transaction
    sql = "INSERT INTO transactions (direction, truck, bruto, datetime,  truckTara, produce) VALUES (%s, %s, %s, %s, %s, %s)"
    date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
    input_data = (direction, truck, bruto, date_time, truckTara, produce)
    cursor.execute(sql, input_data)
    db.commit()
    new_container_id = cursor.lastrowid
    return new_container_id


def register_container(container_id,weight=None,unit=None):
    # adds a new container containers_registered table
    # this function returns the id of the new container
    sql = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
    input_data = (container_id, weight, unit)
    cursor.execute(sql, input_data)
    db.commit()


def update_container(container_id,weight=None,unit=None):
    #updates container data in containers_registered table
    sql = "UPDATE containers_registered SET weight = %s, unit = %s WHERE container_id = %s"
    input_data = (weight, unit, container_id)
    cursor.execute(sql, input_data)
    db.commit()


def insert_new_container_in_transaction(container_id, transaction_id, direction):
    if direction == 'none':
        sql = "INSERT INTO container_in_transaction (container_id, transaction_id_none) VALUES (%s, %s)"
        input_data = (container_id, transaction_id)
        cursor.execute(sql, input_data)
        db.commit()
    elif direction == 'in':
        sql = "INSERT INTO container_in_transaction (container_id, transaction_id_in) VALUES (%s, %s)"
        input_data = (container_id, transaction_id)
        cursor.execute(sql, input_data)
        db.commit()
    else:
        return 'direction wasnt inserted'
    
def get_containers_from_transaction(transaction_id):
    sql = "SELECT container_id FROM container_in_transaction WHERE transaction_id_in = %s OR transaction_id_none = %s OR transaction_id_out = %s"
    input_data = (transaction_id,transaction_id,transaction_id)
    cursor.execute(sql, input_data)
    results = cursor.fetchall()
    container_ids = [result[0] for result in results]
    return container_ids
    


def get_container_weights(transaction_id):
    sql = "SELECT containers_registered.weight FROM containers_registered JOIN container_in_transaction ON containers_registered.container_id = container_in_transaction.container_id WHERE container_in_transaction.transaction_id_in = %s OR container_in_transaction.transaction_id_none = %s"
    input_data = (transaction_id, transaction_id,)
    cursor.execute(sql, input_data)
    results = cursor.fetchall()
    weights = [result[0] for result in results]
    return weights

def get_container_weight(container_id):
    sql = "SELECT weight FROM containers_registered WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    if result[0] == -1:
        return 'na'
    return result[0]
    

def get_neto_weight(transaction_id,neto_weight = -1):
    containers_weights = get_container_weights(transaction_id)
    total_weight = 0
    for weight in containers_weights:
        if weight == -1:
            return 'na'
        else:
            total_weight += weight
    print(total_weight, 'total')
    return total_weight

    

    
def get_transaction_if_out(transaction_id):
    sql = "SELECT transaction_id_out FROM container_in_transaction WHERE transaction_id_in  = %s OR transaction_id_none = %s"
    input_data = (transaction_id, transaction_id)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    
    if result is None:
        return False
    if result[0] is None:
        return 'not out'
    return result[0]

def get_transaction_data(transaction_id):
    sql = "SELECT * FROM transactions WHERE id = %s"
    input_data = (transaction_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    
    if result is None:
        return False
    return {
        'id': result[0],
        'datetime': result[1].strftime('%Y-%m-%d %H:%M:%S') if result[1] else None,
        'direction': result[2],
        'truck': result[3],
        'bruto': result[4] if result[4] is not None else 'na',
        'truckTara': result[5] if result[5] is not None else 'na',
        'produce': result[6]
         }
    
    

    



def handle_force(container_id, direction, new_transaction_id):

    # this part updates the container_in_transaction with new data and return the transaction id that needs to be deleted
    transaction_to_delete_id = update_container_in_transaction(container_id, direction, new_transaction_id)
    
    # this part delets the old transaction
    delete_transaction(transaction_to_delete_id)
    

def update_container_in_transaction(container_id, direction, new_transaction_id):
    # this function gets an container id and direction and delets this record
    # return the transaction id that needs to be deletes from transactions table
    
    # this part finds the current transaction id
    sql = "SELECT transaction_id_in, transaction_id_out, transaction_id_none FROM container_in_transaction WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    
    # this part updates the transaction_id based on direction with the new data
    if(direction == 'in'):
        sql = "UPDATE container_in_transaction SET transaction_id_in = %s WHERE container_id = %s"
        input_data = (new_transaction_id, container_id)
        cursor.execute(sql, input_data)
        db.commit()
        if result is None:
            return False
        return result[0]
    
    if(direction == 'none'):
        sql = "UPDATE container_in_transaction SET transaction_id_none = %s WHERE container_id = %s"
        input_data = (new_transaction_id, container_id)
        cursor.execute(sql, input_data)
        db.commit()
        if result is None:
            return False
        return result[2]
    
    sql = "UPDATE container_in_transaction SET transaction_id_out = %s WHERE container_id = %s"
    input_data = (new_transaction_id, container_id)
    cursor.execute(sql, input_data)
    db.commit()
    if result is None:
        return False
    return result[1]
    


def delete_transaction(transaction_id):
    # this function gets a transaction_id and direaction and delets it from transactions table
    sql = "DELETE FROM transactions WHERE id = %s"
    input_data = (transaction_id, )
    cursor.execute(sql, input_data)
    db.commit()


def check_if_container_id_exsits(container_id):
    
    #this function checks if a container exsits in the containers_registered table

    sql = "SELECT * FROM containers_registered WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    print(result)
    if result is None:
        return False
    else:
        return True

def find_transaction_id(container_id, direction):
    sql = "SELECT transaction_id_in, transaction_id_out FROM container_in_transaction WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    if(direction == 'in'):
        return result[0]
    return result[1]
    #gets container id and gets the transaction id

def get_in_weight(transaction_id):
    sql = "SELECT bruto FROM transactions WHERE id = %s"
    input_data = (transaction_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    return result[0]
    

def check_if_truck_id_is_the_same(truck_id, transaction_id):
    #gets transaction id and truck id 
    #todo: you need to select truck from transactions table where transaction_id=transaction_id
    sql = "SELECT truck FROM transactions WHERE id = %s"
    input_data = (transaction_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    elif result[0] == truck_id:
        print(result[0], 'this the same truck')
        return True
      
    print(result[0], "failed to find truck")
    return False



def check_container_status(container_id):
    #checks if container is in transactions db
    #return if container exsits it's status
    #if container dosn't exsits - return false
    sql = "SELECT transaction_id_in, transaction_id_out,transaction_id_none FROM container_in_transaction WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    if result is None:
        return False
    if result[1]:
        return ['out',result[1], result[0]]
    if result[2]:
        return ['none', result[2]]
    return ['in', result[0]]
    

def handle_container_weight_calculation_from_files(containers, neto_weight = -1):
    
    total_weight = 0
    # the sum of all the weight mof the containers we found
    
    unknown_containers = []
    #a list of all containers id's we didn't find their weight
    
    containers_with_weight = {}
    #a dictionary which each key is an container is and value is it's weighht we found
    
    for container in containers:
        # TODO: csv input here
        result = check.check_if_exists_in_file(container)
        if result is not False:
            containers_with_weight[container] = result
            total_weight += int(result)
        else:
            unknown_containers.append(container)
    if(neto_weight != -1  and len(unknown_containers) == 1):
        containers_with_weight[unknown_containers[0]] = int(neto_weight) - total_weight
    return containers_with_weight



def handle_in(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers_string):
    if truck == '':
            return 'You must enter truck license'
    # this function will handle all logic needed for in action
    #this function will either return a string error or a json of the result
    #The json output od the result will look like:
    #      { "id": <str>, 
    #    "truck": <license> or "na",
    #    "bruto": <int>,
    #  }
    
    containers = [c.strip() for c in containers_string.split(',')]
    # a list of containers, each value represent a container id
    
    errors = []
    # a list of errors to show the user, if stays empty than evrything is valid
    
    force_containers = []
    #a list of containers id that needs to have force action on
    
    new_containers = []
    #a list of containers that are new and needs to be registered
    if(unit_of_measure_bruto == 'lbs'):
        unit_of_measure_bruto = 'kg'
        truck_bruto = int(truck_bruto) * 0.45359237 

    
    for container in containers:
        # This parts goes over all containers and validates them
        if(check_if_container_id_exsits(container)):
            container_status = check_container_status(container)
            if container_status is not False:
                if container_status[0] == 'in':
                    if(force != 'True'):
                        errors.append(container + ' Container already registerd in and force wassnt selected')
                    else:
                        force_containers.append(container)
                elif container_status[0] == 'out':
                    errors.append(container + ' Container already registerd in the system as out')
                else:
                    errors.append(container + 'ontainer already registerd as standalone cotainer')
        else:
            new_containers.append(container)
            
         
    if(len(errors)):
        print(errors)
        #if containers are not valid - return this errors
        return '<br/>'.join(errors)

    containers_weight_found_in_files = handle_container_weight_calculation_from_files(containers) 
    #  containers_weight_found_in_files is a dictionary of all the containers that were found in files
    
    new_transaction_id =  insert_transaction(direction, truck, truck_bruto, produce)
    # create new transaction and return the transaction id
    
    for container in new_containers:

        #create new container(adds weight and unit if found in files)
        new_container_weight = containers_weight_found_in_files.get(container, -1)
        register_container(container, new_container_weight, 'kg')
        
        #connect container to transaction
        insert_new_container_in_transaction(container, new_transaction_id, 'in')

    for container in force_containers:
        new_container_weight = containers_weight_found_in_files.get(container, None)
        if(new_container_weight != None):
            update_container(container,new_container_weight, unit_of_measure_bruto)
        handle_force(container, 'in', new_transaction_id )
        
    return { "id":new_transaction_id , "truck": truck or "na", "bruto": truck_bruto}
    


def handle_out(direction,truck,produce,truck_tara,unit_of_measure_bruto,force,containers_string):
    if truck == '':
            return 'You must enter truck license'
    # this function will handle all logic needed for out action
    #you need to check the container status - if in -> continue, if none - return an error
    #if the status is out -> check if force = true, if force =false return an error
    #if status=out and force=true, override the data
    #this function will either return a string error or a json of the result
    #The json output:
    #      { "id": <str>, 
    #    "truck": <license> or "na",
    #    "bruto": <int>,
    #    ONLY for OUT:
    #    "truckTara": <int>,
    #    "neto": <int> or "na" // na if some of containers have unknown tara
    #  }
    
    containers = containers_string.split(',')
    # a list of containers, each value represent a container id
    
    errors = []
    # a list of errors to show the user, if stays empty than evrything is valid
    
    force_containers = []
    #a list of containers id that needs to have force action on
    
    regular_containers = []
    #a list of containers that are new and needs to be registered

    
    in_transaction_id =''
    #the id of the insert of the container
    
    if(unit_of_measure_bruto == 'lbs'):
        unit_of_measure_bruto = 'kg'
        truck_tara = convert_lbs_to_kg(truck_tara)

   # TODO: 1. validate errors 
    transaction_id_in = find_transaction_id(containers[0], 'in')
    if transaction_id_in is False:
        return 'You have to enter the truck in before you out',400
    if not check_if_truck_id_is_the_same(truck, transaction_id_in):
        return 'The truck id you gave isnnot matching the giver containers'
    
    truck_weight_in = get_in_weight(transaction_id_in)
    if truck_weight_in is False: 
        return 'Truck weight in was not inserted' 
    
    containers_weight = truck_weight_in - int(truck_tara)
    if containers_weight <= 0:
        return 'Truck Weight In is smaller than Truck Weight Out - not possible'
    
    for container in containers:
        # This parts goes over all containers and validates them
        #TODO: 1check if container exsit -> error if not
        #TODO: 2check contianer status(in/out/none) -> if in ->good, if out -> check force -> if force false -> error if false true -> good, if none -> error
        #TODO: 3check if truck_id on in is the same that we got now - else error - we need to build a new functin for this - done!!
        #TODO: 4check if weight in > weight out
        if(check_if_container_id_exsits(container)):
            container_status = check_container_status(container)
            if container_status is not False:
                if container_status[0] == 'in':
                    regular_containers.append(container)
                    in_transaction_id = container_status[1]
                elif container_status[0] == 'out':
                    if(force != 'True'):
                        errors.append(container + " container is already out, force was off")
                    else:
                        force_containers.append(container)
                        in_transaction_id = container_status[1]
                else:
                    errors.append(container + " container is registered as a standalone container with the option 'None'")
        else:
            errors.append(container + " container is not registerd yet")
         
    if(len(errors)):
        print(errors)
        #if containers are not valid - return this errors
        return '<br/>'.join(errors)

    # create new transaction and return the transaction id
    new_transaction_id =  insert_transaction(direction, truck, truck_weight_in, produce, truck_tara)
    containers_neto = int(truck_weight_in) - int(truck_tara)
    containers_weight_found_in_files = handle_container_weight_calculation_from_files(containers,containers_neto) 
    
    if len(containers) == 1:
        new_container_weight = containers_weight_found_in_files.get(containers[0], 'na')
        if new_container_weight == 'na':
            new_container_weight = containers_weight
        else:
            update_container(container, new_container_weight, 'kg') 
    else:   
        for container in containers:
            new_container_weight_from_csv = containers_weight_found_in_files.get(container, -1)
            if new_container_weight_from_csv != -1:
                update_container(container, new_container_weight_from_csv, 'kg')
                
    for container in regular_containers:
        update_container_in_transaction(container, direction, new_transaction_id)
    
    for container in force_containers:
        handle_force(container, direction, new_transaction_id)


    neto = get_neto_weight(transaction_id_in,containers_neto)
    
    return { "id":in_transaction_id , "truck": truck or "na", "bruto": truck_weight_in, "truckTara": truck_tara, "neto": neto}

def handle_none(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers_string):
    
    if truck != '':
        return "a standalone container cannot have a truck registered"  

    containers = [c.strip() for c in containers_string.split(',')]
    # a list of containers, each value represent a container id
    
    errors = []
    # a list of errors to show the user, if stays empty than evrything is valid
    
    force_containers = []
    #a list of containers id that needs to have force action on
    
    new_containers = []
    #a list of containers that are new and needs to be registered
    
    if(unit_of_measure_bruto == 'lbs'):
        unit_of_measure_bruto = 'kg'
        truck_bruto = convert_lbs_to_kg(truck_bruto)

    
    for container in containers:
        # This parts goes over all containers and validates them

        if(check_if_container_id_exsits(container)):
            container_status = check_container_status(container)
            if container_status is not None:
                errors.append(container + "a truck already registered this container")
            elif force != 'True':
                errors.append(container + " container is already registerd as none, force was off")
            else:
                force_containers.append(container)
        else:
            new_containers.append(container)
   
    if(len(errors)):
        return '<br/>'.join(errors)
    
    containers_weight_found_in_files = handle_container_weight_calculation_from_files(containers)
    new_transaction_id =  insert_transaction(direction, 'none', truck_bruto, produce)
    
    if len(containers) == 1:
        new_container_weight = containers_weight_found_in_files.get(container, truck_bruto)
        if len(new_containers) == 1:
            register_container(container, new_container_weight, 'kg')
            insert_new_container_in_transaction(container, new_transaction_id, 'none')
            
        else:
            update_container(container,new_container_weight, 'kg')
            handle_force(container, 'none', new_transaction_id )
            
        neto = get_neto_weight(new_transaction_id)  
        return {"id":new_transaction_id , "truck": 'none', "bruto": neto}


    
    for container in new_containers:
        #create new container(adds weight and unit if found in files)
        new_container_weight = containers_weight_found_in_files.get(container, -1)
        register_container(container, new_container_weight, 'kg')
        
        #connect container to transaction
        insert_new_container_in_transaction(container, new_transaction_id, 'none')

    for container in force_containers:
        new_container_weight = containers_weight_found_in_files.get(container, -1)
        update_container(container,new_container_weight, unit_of_measure_bruto)
        handle_force(container, 'none', new_transaction_id )
        
    neto = get_neto_weight(new_transaction_id)
    return { "id":new_transaction_id , "truck": 'none', "bruto": neto}

def get_session_data(session_id):
    in_transaction_data = get_transaction_data(session_id)
    if in_transaction_data is False:
        return '404'
    out_transaction_id = get_transaction_if_out(session_id)
    if out_transaction_id == 'not out':
        return { "id":session_id , "truck": in_transaction_data['truck'], "bruto": in_transaction_data['bruto']} 
    if out_transaction_id is not False:
        out_transaction_data = get_transaction_data(out_transaction_id)
        neto = get_neto_weight(session_id)
        return { "id":session_id , "truck": in_transaction_data['truck'], "bruto": in_transaction_data['bruto'], "truckTara":out_transaction_data['truckTara'] ,"neto":neto} 
    return 'unknown error'

def handle_get_data_between_dates(start_date, end_date, filter):
    transactions = get_transactions_by_date_range(start_date, end_date, filter)
    if len(transactions) == 0:
        return 'No transactions found'
    results = []
    for transaction in transactions:
        containers = get_containers_from_transaction(transaction['id'])
        neto = get_neto_weight(transaction['id'])
        results.append(f"id: {transaction['id']}, direction: {transaction['direction']}, bruto: {transaction['bruto']}, neto: {neto}, produce: {transaction['produce']}, containers: {containers}")
    return '<br/>'.join(results)


def handle_get_item(id,start_date, end_date):
    container = check_container_status(id)
    tara = ''
    sessions =[]
    if container is False:
        truck_transactions = get_transactions_by_date_range_for_truck(id,start_date, end_date)
        if len(truck_transactions) == 0:
            return 'no transactions found'
        sessions = [t['id'] for t in truck_transactions]
        tara = get_last_known_tara(id,start_date, end_date)
        return {"id": id ,"tara": tara ,"sessions": sessions }
    else:
        tara = get_container_weight(id)
        if container[0] == 'none' or 'in':
            transaction_in_date = check_if_container_transaction_between_dates(container[1], start_date, end_date)
            sessions = [container[1]]
        elif container[0] == 'out':
            transaction_in_date = check_if_container_transaction_between_dates(container[1], start_date, end_date)
            sessions = [container[2]]
        else:
            sessions = [container[1]]
            
        if transaction_in_date is False:
            return 'The transaction for this container is not between those dates'
    return {"id": id ,"tara": tara ,"sessions": sessions }
    



def unknown():
    arr=[]
    db=get_connection()
    cursor=db.cursor()
    sql= "SELECT * FROM containers_registered"
    cursor.execute(sql)
    data=cursor.fetchall()
    for i in data:
        if i[1]==-1:
            arr.append(i[0])

    return arr
