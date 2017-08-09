import sqlite3



# Inserting audiologist login information into database
def save_audiologist_to_database(audiologist, email, username, password):
    conn = sqlite3.connect('audiologist-login.db')
    d = conn.cursor()
    d.execute('INSERT INTO audiologists (audiologist, email, username, password)'
              'VALUES (?, ?, ?, ?)', (audiologist, email, username, password))
    # Saving inserted data in database
    conn.commit()
    d.close()


# Function allowing insertion of refer patient data into database
def save_refer_patient_to_database(last_name, first_name, MOC_last_name, MOC_first_name,
                                    DOB, MOC_DOB, street, city, zip_code, pediatrician,
                                    delivery_hospital, refer_screening, refer_ear, technician_initials,
                                    risk_factors, Epic_note, Epic_order, fax, follow_up_appointment_location,
                                    follow_up_appointment_date, follow_up_results, hearing_loss_ear,
                                    hearing_loss_severity):

    conn = sqlite3.connect('2017-refer-database.db')
    d = conn.cursor()
    d.execute(''' INSERT INTO refers (last_name, first_name, MOC_last_name, MOC_first_name,
              DOB, MOC_DOB, street, city, zip_code, pediatrician,
              delivery_hospital, refer_screening, refer_ear, technician_initials,
              risk_factors, Epic_note, Epic_order, fax, follow_up_appointment_location,
              follow_up_appointment_date, follow_up_results, hearing_loss_ear,
              hearing_loss_severity)'''
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (last_name, first_name, MOC_last_name, MOC_first_name, DOB, MOC_DOB, street, city, zip_code, pediatrician,
                delivery_hospital, refer_screening, refer_ear, technician_initials,
                risk_factors, Epic_note, Epic_order, fax, follow_up_appointment_location, follow_up_appointment_date, follow_up_results, hearing_loss_ear,
                hearing_loss_severity))
    conn.commit()
    d.close()


# Function allowing audiologist to login to enter and/or access patient data
def login(username, password):
    entered_username = str(username)
    entered_password = str(password)

    # Connecting to database of audiologist login information & fetching the username and password rows that match the user-entered username & password
    conn = sqlite3.connect('audiologist-login.db')
    d = conn.cursor()
    d.execute("SELECT * from audiologists WHERE username=:username AND password=:password",
              {"username": entered_username, "password": entered_password})
    database_user = d.fetchone()
    d.close()


    # Ensuring entered username & password match an entry in the conn_audiologists database
    if database_user is not None:
        return True
    else:
        return False




# Function allowing audiologist to edit patient data in refer entry
# def edit_refer_entry

# Function allowing audiologist to delete refer entry
# def delete_refer_entry

# Function allowing audiologist to search patient data in refer database
def search_refer_database(search_term):
    search_term = (search_term,)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all entries containing search_term within refers database
    d = conn.cursor()
    all_rows = d.execute('SELECT * from refers')
    for row in all_rows:
        if row == search_term:
            print row


def main():
    # CREATING DATABASES
    # Database of audiologists who will be entering data
    conn_audiologists = sqlite3.connect('audiologist-login.db')

    # Database of refer patient data
    conn_refers = sqlite3.connect('2017-refer-database.db')

    # Creating database of audiologist login user information (ref: https://docs.python.org/2/library/sqlite3.html)
    c = conn_audiologists.cursor()
    c.execute(
        ''' CREATE TABLE IF NOT EXISTS audiologists (audiologist text, email text, username text, password text) ''')
    # This is repetitive - improve?
    save_audiologist_to_database('Krysta_Gasser_Rutledge', 'krysta@ormonitoringconsultants.com', 'kgasser', 'hearing1')
    save_audiologist_to_database('Megan_Terry_Kelly', 'megankelly@thehearingconsultants.com', 'mkelly', 'hearing2')
    save_audiologist_to_database('Sarah_Chandler', 'sarahchandler@thehearingconsultants.com', 'schandler', 'hearing3')
    save_audiologist_to_database('Anne_Murray', 'annemurray@thehearingconsultants.com', 'amurray', 'hearing4')
    save_audiologist_to_database('Karen_Tutt', 'karentutt@thehearingconsultants.com', 'ktutt', 'hearing5')
    save_audiologist_to_database('Lexi_Kirner', 'lexi@thehearingconsultants.com', 'lkirner', 'hearing6')
    save_audiologist_to_database('Tracy_Mishler', 'tracy@thehearingconsultants.com', 'tmishler', 'hearing7')
    # Closing connection
    c.close()

    # Creating database of patient information for those babies who referred on his/her newborn hearing screening
    c = conn_refers.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS refers (id integer primary key autoincrement, last_name text, first_name text,
              MOC_last_name text, MOC_first_name text,
              DOB date, MOC_DOB date, street text, city text, zip_code integer, pediatrician text,
              delivery_hospital text, refer_screening text, refer_ear text, technician_initials text,
              risk_factors text, Epic_note text, Epic_order text, fax text, follow_up_appointment_location text,
              follow_up_appointment_date date, follow_up_results text, hearing_loss_ear text,
              hearing_loss_severity text) ''')
    # Saving database
    conn_refers.commit()
    # Closing connection
    c.close()

    # User must input username & password to access data in refer database
    login_status = False
    while login_status == False:
        username = str(raw_input("Type a username: "))
        password = str(raw_input("Type a password: "))
        login_status = login(username, password)
        if login_status == False:
            print "Username and/or password is not valid, please try again and/or contact administrator for updated credentials"
        else:
            print "Welcome to Newborn Hearing Services"

    # User must input patient data into refer database (future improvement: make class to represent refer data entry)
    # last_name = raw_input("Patient's Last Name: ")
    # first_name = raw_input("Patient's First Name: ")
    # MOC_last_name = raw_input("Mother of Child's (MOC) Last Name: ")
    # MOC_first_name = raw_input("MOC's First Name: ")
    # DOB = raw_input("Patient's date of birth (DOB): ")
    # MOC_DOB = raw_input("MOC's DOB: ")
    # street = raw_input("Patient's address (street number & name): ")
    # city = raw_input("Patient's address (city): ")
    # zip_code = int(raw_input("Patient's zip code: "))
    # pediatrician = raw_input("Patient's pediatrician/primary care physician: ")
    # delivery_hospital = raw_input("Hospital at which MOC delivered: ")
    # refer_screening = raw_input("Patient referred on which screening (DPOAE, ABAER, or miss): ")
    # refer_ear = raw_input("Patient referred in which ear (R, L, or AU): ")
    # technician_initials = raw_input("Technician initials of tech who performed screening: ")
    # risk_factors = raw_input("Patient risk factor(s) for newborn hearing loss: ")
    # Epic_note = raw_input("Epic note created (Y, N, or pending): ")
    # Epic_order = raw_input("Epic order created (Y, N, or CNE): ")
    # fax = raw_input("Pediatrician faxed (Y, N, or pending): ")
    # follow_up_appt_location = raw_input("Follow-up appointment location: ")
    # follow_up_appt_date = raw_input("Follow-up appointment date: ")
    # follow_up_results = raw_input("Follow-up results, entered by ear & frequencies tested: ")
    # hearing_loss_ear = raw_input("If hearing loss is present, which ear (R, L, or AU): ")
    # hearing_loss_severity = raw_input(
    #         "If hearing loss is present, which severity (mild, moderate, moderately-severe, severe, profound): ")

    last_name ='Smith'
    first_name ='John'
    MOC_last_name ='Smith'
    MOC_first_name ='Mary'
    DOB ='7/18/2017'
    MOC_DOB ='1/18/1997'
    street ='1234 Happy Hills Ln.'
    city ='St. Louis'
    zip_code ='63122'
    pediatrician ='Saville, Brian'
    delivery_hospital ='DPL'
    refer_screening ='ABAER'
    refer_ear ='AU'
    technician_initials ='MJ'
    risk_factors ='Craniofacial anomaly'
    Epic_note ='Y'
    Epic_order ='Y'
    fax ='Y'
    follow_up_appt_location ='DPL'
    follow_up_appt_date ='8/8/2017'
    follow_up_results ='Pending'
    hearing_loss_ear ='Pending'
    hearing_loss_severity ='Pending'

    # Saving refer entry just entered
    save_refer_patient_to_database(last_name, first_name, MOC_last_name, MOC_first_name, DOB, MOC_DOB, street, city,
    zip_code, pediatrician, delivery_hospital, refer_screening, refer_ear, technician_initials,
    risk_factors, Epic_note, Epic_order, fax, follow_up_appt_location, follow_up_appt_date,
    follow_up_results, hearing_loss_ear, hearing_loss_severity)

    # Printing refer entry just entered
    print search_refer_database(last_name)

    reroute = raw_input('Would you like to return to the main database (Y or N)?: ')
    if reroute == 'Y':
        # Print database
        conn = sqlite3.connect('2017-refer-database.db')
        d = conn.cursor()
        for row in d.execute('SELECT * from refers ORDER BY DOB'):
            print row


if __name__ == "__main__":
    main()
