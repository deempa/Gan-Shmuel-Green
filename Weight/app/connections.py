import mysql.connector
from datetime import datetime, date
import check

def get_connection():
    db = mysql.connector.connect(
         host="localhost",
        # host="weight-db"
        user="root",
        port=3300,
        password="123",
        database="weight"
    )

    return db

db = get_connection()
cursor = db.cursor()

def insert_transaction(direction, truck, bruto, produce, truckTara=None):
    # this function inserts a new transaction to transactions table
    # this function returns the id of the new transaction
    sql = "INSERT INTO transactions (direction, truck, bruto, datetime,  truckTara, produce) VALUES (%s, %s, %s, %s, %s, %s)"
    date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
    input_data = (direction, truck, bruto, date_time, truckTara, produce)
    cursor.execute(sql, input_data)
    db.commit()
    new_container_id = cursor.lastrowid
    print(new_container_id, 'new_container_id creation')
    return new_container_id





def register_container(container_id,weight=None,unit=None):
    # adds a new container containers_registered table
    # this function returns the id of the new container
    sql = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
    input_data = (container_id, weight, unit)
    cursor.execute(sql, input_data)
    db.commit()
    print(cursor.lastrowid, 'new_container_id creation')

def update_container(container_id,weight=None,unit=None):
    #updates container data in containers_registered table
    sql = "UPDATE containers_registered SET weight = %s, unit = %s WHERE container_id = %s"
    input_data = (weight, unit, container_id)
    cursor.execute(sql, input_data)
    db.commit()


def insert_new_container_in_transaction(container_id, transaction_id_in):
    print(container_id, transaction_id_in, 'new cont in tran')
    sql = "INSERT INTO container_in_transaction (container_id, transaction_id_in) VALUES (%s, %s)"
    input_data = (container_id, transaction_id_in)
    cursor.execute(sql, input_data)
    db.commit()


def handle_force(container_id, direction, new_transaction_id):

    # this part updates the container_in_transaction with new data and return the transaction id that needs to be deleted
    transaction_to_delete_id = update_container_in_transaction(container_id, direction, new_transaction_id)
    print(transaction_to_delete_id, 'delete transaction')
    
    # this part delets the old transaction
    delete_transaction(transaction_to_delete_id)
    

def update_container_in_transaction(container_id, direction, new_transaction_id):
    # this function gets an container id and direction and delets this record
    # return the transaction id that needs to be deletes from transactions table
    
    # this part finds the current transaction id
    sql = "SELECT transaction_id_in, transaction_id_out FROM container_in_transaction WHERE container_id = %s"
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
    sql = "SELECT transaction_id_in, transaction_id_out FROM container_in_transaction WHERE container_id = %s"
    input_data = (container_id,)
    cursor.execute(sql, input_data)
    result = cursor.fetchone()
    print(container_id, 'id of container')
    print(result)
    if result is None:
        return False
    if result[1]:
        return 'out'
    return 'in'
    

def handle_container_weight_calculation_from_files(containers, neto_weight = False):
    
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
        
    if(neto_weight and len(unknown_containers) == 1):
        containers_with_weight[unknown_containers[0]] = neto_weight - result
    return containers_with_weight

def calculate_container_weight():
    #this function calculates the container weight
    pass


def handle_in(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers_string):
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
        print(check_if_container_id_exsits(container), container, 'check me')
        if(check_if_container_id_exsits(container)):
            container_status = check_container_status(container)
            print(container_status, 'con status')
            if(container_status == 'in'):
                print(force, 'force value')
                if(force != 'True'):
                    errors.append(container + ' Container already registerd in and force wassnt selected')
                else:
                    force_containers.append(container)
            elif (container_status == 'out'):
                errors.append(container + ' Container already registerd in the system as out')
            else:
                errors.append(container + ' container already registerd')
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
        unit_of_measure = unit_of_measure_bruto if new_container_weight != -1 else None
        register_container(container, new_container_weight, unit_of_measure)
        
        #connect container to transaction
        insert_new_container_in_transaction(container, new_transaction_id)

    for container in force_containers:
        new_container_weight = containers_weight_found_in_files.get(container, None)
        if(new_container_weight != None):
            update_container(container,new_container_weight, unit_of_measure_bruto)
        handle_force(container, 'in', new_transaction_id )
        
    return { "id":new_transaction_id , "truck": truck or "na", "bruto": truck_bruto}
    


def handle_out(direction,truck,produce,truck_tara,unit_of_measure_bruto,force,containers_string):
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
    
    neto = ''
    #for output - dictinoary of the container id as key and their weight as the value
    if(unit_of_measure_bruto == 'lbs'):
        unit_of_measure_bruto = 'kg'
        truck_tara = int(truck_tara) * 0.45359237 

   # TODO: 1. validate errors 
    transaction_id_in = find_transaction_id(containers[0], 'in')
    if transaction_id_in is False:
        return ('You have to enter the truck in before you out',400)
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
            if container_status == 'in':
                regular_containers.append(container)
            elif container_status == 'out':
                if(force != 'True'):
                    errors.append(container + " container is already out, force was off")
                else:
                    force_containers.append(container)
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
    containers_weight_found_in_files = handle_container_weight_calculation_from_files(containers) 
    
    if len(containers) == 1:
        new_container_weight = containers_weight_found_in_files.get(containers[0], 'na')
        if new_container_weight == 'na':
            new_container_weight = containers_weight
        update_container(containers[0], new_container_weight, unit_of_measure_bruto)   
        neto = {containers[0]: new_container_weight}      
    else:   
        neto = containers_weight_found_in_files
        for container in containers:
            new_container_weight_from_csv = containers_weight_found_in_files.get(container, -1)
            if new_container_weight_from_csv != -1:
                pass
            else:
                update_container(container, new_container_weight_from_csv, unit_of_measure_bruto)
    print(force_containers, 'force')
    print(regular_containers, 'regular')    
    for container in regular_containers:
        update_container_in_transaction(container, direction, new_transaction_id)
    
    for container in force_containers:
        handle_force(container, direction, new_transaction_id)
        
            
        
        
        
        # TODO: 1.a if there's no 'in' to said container
        # TODO: 1.b if the force is 'off' and container status is 'out'
        # TODO: 1.c if the weight given to the truck is bigger at 'out' then at 'in'
        # TODO: 1.d if the truck at status 'out' does not match any truck at status 'in' (meaning the truck never came in)
    
    # TODO: 2. normal response (this is an out followed by a normal in)
        # TODO: 2.a check if the status of the container, if it was 'in' then insert the data
        # TODO: 2.b calculate the weight of the containers the truck has delivered and insert known data to the database
        # TODO: 2.c return the needed json 
        
    # TODO: 3. an out followed by out with force on (rewrite last out of the same container) 
        # TODO: 3.a rewrite the needed data in the database to match the new input
        # TODO: 3.b calculate the weight of the containers the truck has delivered and insert known data to the database
        # TODO: 3.c return the needed json
        

    return { "id":new_transaction_id , "truck": truck or "na", "bruto": truck_weight_in, "truckTara": truck_tara, "neto": neto}

def handle_none(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers):
    # "none" after "in" will generate error
    #if truck -> error
    #if force off -> and container registerd -> error
    pass

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