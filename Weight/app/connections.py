import mysql.connector

from datetime import datetime, date



def get_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3300,
        password="123",
        database="weight"
    )

    return db

db = get_connection()
cursor = db.cursor()

def insert_transaction(direction, truck, bruto, produce, truckTara=None, neto=None):
    # this function inserts a new transaction to transactions table
    # this function returns the id of the new transaction
    sql = "INSERT INTO transactions (direction, truck, bruto, datetime,  truckTara, neto, produce) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
    input_data = (direction, truck, bruto, date_time, truckTara, neto, produce)
    with db.cursor() as cursor:
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

def update_container_in_transaction_out(container_id, transaction_id_out):
    # TODO: THIS IS READY JUST USE IT 
    sql = "UPDATE container_in_transaction SET transaction_id_out = %s WHERE container_id = %s"
    input_data = (transaction_id_out, container_id)
    cursor.execute(sql, input_data)
    db.commit()

def handle_force(container_id, direction, new_transaction_id):

    # this part updates the container_in_transaction with new data and return the transaction id that needs to be deleted
    transaction_to_delete_id = update_container_in_transaction(container_id, direction, new_transaction_id)
    
    # this part delets the old transaction
    delete_transaction(transaction_to_delete_id, direction)
    

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
        return result[0]
    sql = "UPDATE container_in_transaction SET transaction_id_out = %s WHERE container_id = %s"
    input_data = (new_transaction_id, container_id)
    cursor.execute(sql, input_data)
    db.commit()
    return result[1]
    


def delete_transaction(transaction_id, direction):
    # this function gets a transaction_id and direaction and delets it from transactions table
    sql = "DELETE FROM transactions WHERE id = %s AND direction = %s"
    input_data = (transaction_id, direction)
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
        # TODO: do the logic that searches in the file - VLAD PART
        # TODO: update found weight to the founding from the csv file - VLAD PART
        found_weight = 0 
        if found_weight:
            containers_with_weight[container] = found_weight
            total_weight += found_weight
        else:
            unknown_containers.append(container)
        
    if(neto_weight and len(unknown_containers) == 1):
        containers_with_weight[unknown_containers[0]] = neto_weight - found_weight
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
    
    containers = containers_string.split(',')
    # a list of containers, each value represent a container id
    
    errors = []
    # a list of errors to show the user, if stays empty than evrything is valid
    
    force_containers = []
    #a list of containers id that needs to have force action on
    
    new_containers = []
    #a list of containers that are new and needs to be registered

    
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
        #if containers are not valid - return this errors
        return '<br/>'.join(errors)
    
    containers_weight_found_in_files = handle_container_weight_calculation_from_files(containers) 
    #  containers_weight_found_in_files is a dictionary of all the containers that were found in files
    
    for container in new_containers:

        # create new transaction and return the transaction id
        new_transaction_id =  insert_transaction(direction, truck, truck_bruto, produce)
        
        #create new container(adds weight and unit if found in files)
        new_container_weight = containers_weight_found_in_files.get(container, -1)
        unit_of_measure = unit_of_measure_bruto if new_container_weight == -1 else None
        register_container(container, new_container_weight, unit_of_measure)
        
        
        #connect container to transaction
        insert_new_container_in_transaction(container, new_transaction_id)

    for container in force_containers:
        new_container_weight = containers_weight_found_in_files.get(container, None)
        if(new_container_weight != None):
            update_container(container,new_container_weight, unit_of_measure_bruto)
        new_transaction_id = insert_transaction(direction, truck, truck_bruto, produce)
        handle_force(container, 'in', new_transaction_id )
        
    return { "id":new_transaction_id , "truck": truck or -1, "bruto": truck_bruto}
    


def handle_out(truck_license,product_delivered,truck_bruto_weight,unit_of_measure_bruto,truck_neto_weight,unit_of_measure_neto,timestamp,container_id):
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
    # TODO:
    return ''

def insert_transaction(direction,truck,containers, truck_bruto,
                       unit_of_measure_bruto,produce,datetime,force):
    
        
        
    db=get_connection()
    cursor=db.cursor()
    sql = "INSERT INTO transactions (direction, truck, containers, bruto, truckTara, neto, produce, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    containers_str=",".join(containers)

    val=(direction,truck,containers_str,truck_bruto,-1,-1,produce,datetime)
    
    cursor.execute(sql,val)
    db.commit
    
    
    for i in containers:
        register_container(container_id=i,wieght=-1,unit=unit_of_measure_bruto)

        
    sql= "SELECT * FROM transactions"
    cursor.execute(sql)
    data=cursor.fetchall()
    for row in data:
        print (row)

    sql= "SELECT * FROM containers_registered"
    cursor.execute(sql)
    data= cursor.fetchall()
    for i in data:
        print(i)


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