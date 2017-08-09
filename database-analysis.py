import sqlite3

# Function calculating total census for 5 delivery hospitals
def total_census(dpl_census, schc_census, sjhw_census, sjsc_census, smhc_census):
    census = dpl_census + schc_census + sjhw_census + sjsc_census + smhc_census
    return census


# Function calculating refer rate by delivery hospital
def refer_rate_hospital(hospital, hospital_census):
    rr_hospital = (hospital, )

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients by hospital from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE delivery_hospital =?', rr_hospital)
    refer_data = d.fetchall()

    refer_rate = (len(refer_data)/hospital_census*100)
    d.close()
    return str(refer_rate) + "%"

# Function calculating refer rate overall (5 delivery hospitals)
def refer_rate_overall(dpl_census, schc_census, sjhw_census, sjsc_census, smhc_census):
    tc = total_census(dpl_census, schc_census, sjhw_census, sjsc_census, smhc_census)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers')
    refer_data = d.fetchall()

    refer_rate = ((len(refer_data) / tc)*100)
    d.close()
    return str(refer_rate) + "%"

# Function calculating missed babies by delivery hospital
def missed_babies_hospital(hospital):
    hospital = (hospital,)
    missed = ('missed',)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all missed patients by hospital from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE delivery_hospital =? AND refer_ear = "missed"', hospital)
    missed_data_hospital = d.fetchall()
    d.close()

    return str(len(missed_data_hospital))


# Function calculating missed babies overall
def missed_babies_overall():
    missed = ('missed',)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all missed patients by hospital from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE refer_ear =?', missed)
    missed_data_overall = d.fetchall()
    d.close()

    return str(len(missed_data_overall))

# Function calculating follow-up (f/u) rate by hospital
def follow_up_rate_hospital(hospital):
    hospital = (hospital,)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients who completed follow-up testing by hospital from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE delivery_hospital =? AND follow_up_appointment_date IS NOT Null', hospital)
    follow_up_data = d.fetchall()

    d.execute('SELECT * from refers WHERE delivery_hospital =?', hospital)
    refer_data = d.fetchall()

    if len(refer_data) == 0:
        d.close()
        return "There are no patients who need follow-up testing at this hospital for the current month (no refers)"

    else:
        follow_up_rate_hospital = (len(follow_up_data) / len(refer_data)*100)
        d.close()
        return str(follow_up_rate_hospital) + "%"

# Function calculating f/u rate overall
def follow_up_rate_overall():

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients who completed follow-up testing from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE follow_up_appointment_date IS NOT Null')
    follow_up_data = d.fetchall()

    d.execute('SELECT * from refers')
    refer_data = d.fetchall()

    if len(refer_data) == 0:
        d.close()
        return "There are no patients who need follow-up testing for the current month (no refers)"
    else:
        follow_up_rate_overall = (len(follow_up_data) / len(refer_data)*100)
        d.close()
        return str(follow_up_rate_overall) + "%"

# Function calculating lost to f/u by hospital
def lost_to_follow_up_hospital(hospital):
    hospital = (hospital,)

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients who did not complete follow-up testing by hospital from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE delivery_hospital =? AND follow_up_appointment_date IS Null', hospital)
    lost_data = d.fetchall()

    d.execute('SELECT * from refers WHERE delivery_hospital =?', hospital)
    refer_data = d.fetchall()

    if len(refer_data) == 0:
        d.close()
        return "There are no patients who are lost to follow-up at this hospital for the current month"
    else:
        lost_rate_hospital = len(lost_data) / len(refer_data)
        d.close()
        return str(lost_rate_hospital) + "%"


# Function calculating lost to f/u overall
def lost_to_follow_up_overall():

    conn = sqlite3.connect('2017-refer-database.db')
    # Select all refer patients who did not complete follow-up testing from refers database
    d = conn.cursor()
    d.execute('SELECT * from refers WHERE follow_up_appointment_date IS Null')
    follow_up_data = d.fetchall()

    d.execute('SELECT * from refers')
    refer_data = d.fetchall()

    if len(refer_data) == 0:
        d.close()
        return "No babies were lost to follow-up this month"
    else:
        lost_rate_overall = (len(follow_up_data) / len(refer_data)*100)
        d.close()
        return str(lost_rate_overall) + "%"

def single_s_sub(message,s):
    return message % s

def main():
    # User must input census values for each hospital (future improvement: direct uploading of this data from other database)
    dpl_census = input("HC census at DPL this month: ")
    schc_census = input("HC census at SCHC this month: ")
    sjhw_census = input("HC census at SJHW this month: ")
    sjsc_census = input("HC census at SJSC this month: ")
    smhc_census = input("HC census at SMHC this month: ")

    # Calculating & displaying total census to user
    census = str(total_census(dpl_census, schc_census, sjhw_census, sjsc_census, smhc_census))
    census_message = "The total HC census for this month is: " + census
    print census_message

    # Visually spacing console-printed results
    print "---------------------------------------------------------------------------------------------------"

    # Calculating & displaying refer rate by hospital to user
    hospitals = (("DPL", dpl_census), ("SCHC", schc_census), ("SJHW", sjhw_census), ("SJSC", sjsc_census), ("SMHC", smhc_census))
    for (h, c) in hospitals:
        h_refer_rate = refer_rate_hospital(h, c)
        message = "The refer rate at %s this month is: "
        refer_rate_message = single_s_sub(message, h)
        print refer_rate_message + str(h_refer_rate)

    # Calculating & displaying overall refer rate to user
    r = refer_rate_overall(dpl_census, schc_census, sjhw_census, sjsc_census, smhc_census)
    print "The overall refer rate for this month is: " + str(r)

    # Visually spacing console-printed results
    print "---------------------------------------------------------------------------------------------------"

    # Calculating & displaying number of missed babies by hospital to user
    hospitals = "DPL", "SCHC", "SJHW", "SJSC", "SMHC"
    for h in hospitals:
        h_missed = missed_babies_hospital(h)
        message = "The number of babies missed at %s this month is: "
        missed_message = single_s_sub(message,h)
        print missed_message + str(h_missed)

    # Calculating & displaying total number of missed babies to user
    m = missed_babies_overall()
    print "The overall number of babies missed for this month is: " + str(m)

    # Visually spacing console-printed results
    print "---------------------------------------------------------------------------------------------------"

    # Calculating & displaying follow-up rate in those patients who referred to user
    for h in hospitals:
        h_follow_up_rate = follow_up_rate_hospital(h)
        message = "The follow-up rate at %s this month is: "
        follow_up_message = single_s_sub(message, h)
        print follow_up_message + str(h_follow_up_rate)

    # Calculating & displaying overall follow-up rate in those patients who referred to user
    f = follow_up_rate_overall()
    print "The overall follow up rate for this month is: " + str(f)

    # Visually spacing console-printed results
    print "---------------------------------------------------------------------------------------------------"

    # Calculating & displaying lost to follow-up rate by hospital to user
    for h in hospitals:
        h_lost_rate = lost_to_follow_up_hospital(h)
        message = "The lost to follow-up rate at %s this month is: "
        lost_message = single_s_sub(message, h)
        print lost_message + str(h_lost_rate)

    # Calculating & displaying overall lost to follow-up rate to user
    l = lost_to_follow_up_overall()
    print "The overall lost to follow-up rate this month is: " + str(l)

    # Visually spacing console-printed results
    print "---------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
    main()





