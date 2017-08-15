import pandas as pd
import sqlite3

# Printing refer database as DataFrame
def print_refer_database_pd():
    # Fetching all patient data in refers database
    conn = sqlite3.connect('2017-refer-database.db')
    df = pd.read_sql_query('SELECT * FROM refers ORDER BY DOB', conn)
    return df

print print_refer_database_pd()

# Function performing descriptive statistics on the following patient variables: 1) Maternal age, 2) Zip code, 3) Delivery hospital,
# 4) Risk Factors, 5) Hearing loss severity (maybe, depending on n)

# Function print histograms of descriptive statistics for patient variables listed above (1-5)

# Function allowing correlational analyses between all patient varaibles