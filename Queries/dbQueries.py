import pandas as pd
import mysql.connector
from pandas.io.sql import DatabaseError
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
DB_HOST=os.environ.get("DB_HOST")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB=os.environ.get("DB")

# db = mysql.connector.connect(
#   host=DB_HOST,
#   user=DB_USER,
#   password=DB_PASSWORD,
#   database=DB
# )
# cursor = db.cursor()


# def add_server(domain, server):
#     sql = "UPDATE domains SET mosaic_server = %s WHERE domain = %s"
#     val = (server, domain)
#     cursor.execute(sql,val)
#     db.commit()
#     print(domain, " Updated")


def get_domains():
    db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM domains")
    result = cursor.fetchall()
    # print(len(result))
    domains = []
    for x in result:
        # print(x)
        # break
        x = list(x)
        href = x[1].replace('https://','').replace('.','~')
        x.append(href)
        domains.append(x)
    # for x in result:
    #     domains.append(str(x).replace('(',"").replace(')','').replace(',','').replace('\'',''))
    # print(domains)
    cursor.close()
    db.close()

    return domains
# get_domains()


def get_single_domain(domain):
    
    #  UNION SELECT * FROM google_page_speed WHERE domain = {domain}
    try:
        db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB
        )
        cursor = db.cursor()
    
    #     cursor.execute(f"SELECT * FROM gtmetrix WHERE domain = '{domain}'")
    # #     # cursor.execute(f"SELECT * FROM google_page_speed WHERE domain = '{domain}'")

    #     result = cursor.fetchall()
    # #     columns = [i[0] for i in cursor.description]
    # #     print(len(columns))
    #     for index, val in enumerate(result):
    #         return val

    # except:
    #     print('error')

        single_ps_df = pd.read_sql_query(f"SELECT * FROM google_page_speed WHERE domain = '{domain}';",con=db)
        single_ps_df['first_contentful_paint'] = single_ps_df['first_contentful_paint'] / 1000
        single_ps_df['time_to_interactive'] = single_ps_df['time_to_interactive'] / 1000
        # single_ps_df['speed_index'] = single_ps_df['speed_index'] / 1000
        single_ps_df['total_blocking_time'] = single_ps_df['total_blocking_time'] / 1000
        single_ps_df['largest_contentful_paint'] = single_ps_df['largest_contentful_paint'] / 1000
        single_ps_df['cumulative_layout_shift'] = single_ps_df['cumulative_layout_shift'] / 1000
        single_ps_df['server_response_time'] = single_ps_df['server_response_time'] / 1000
        single_ps_df['first_meaningful_paint'] = single_ps_df['first_meaningful_paint'] / 1000
        single_ps_df['measurement_date'] = pd.to_datetime(single_ps_df['measurement_date']).dt.date.astype(str)

        single_ps_df = single_ps_df.drop(columns=['speed_index'])

        single_gt_df = pd.read_sql_query(f"SELECT * FROM gtmetrix WHERE domain = '{domain}';",con=db)
        single_gt_df['time_to_first_byte'] = single_gt_df['time_to_first_byte'] / 1000
        # single_gt_df['first_paint_time'] = single_gt_df['first_paint_time'] / 1000
        # single_gt_df['onload_time'] = single_gt_df['onload_time'] / 1000
        # single_gt_df['redirect_duration'] = single_gt_df['redirect_duration'] / 1000
        # single_gt_df['speed_index'] = single_gt_df['speed_index'] / 1000
        single_gt_df['dom_interactive_time'] = single_gt_df['dom_interactive_time'] / 1000
        single_gt_df['first_contentful_paint'] = single_gt_df['first_contentful_paint'] / 1000
        # single_gt_df['total_blocking_time'] = single_gt_df['total_blocking_time'] / 1000
        single_gt_df['largest_contentful_paint'] = single_gt_df['largest_contentful_paint'] / 1000
        single_gt_df['time_to_interactive'] = single_gt_df['time_to_interactive'] / 1000
        single_gt_df['cumulative_layout_shift'] = single_gt_df['cumulative_layout_shift'] / 1000
        single_gt_df['fully_loaded_time'] = single_gt_df['fully_loaded_time'] / 1000
        single_gt_df['measurement_date'] = pd.to_datetime(single_gt_df['measurement_date']).dt.date.astype(str)
        # print(single_gt_df)
        # print(single_ps_df)
        single_gt_df = single_gt_df.drop(columns=['first_paint_time','onload_time','redirect_duration', 'speed_index','total_blocking_time'])

        single_gt_df = single_gt_df.to_dict(orient='records')
        single_ps_df = single_ps_df.to_dict(orient='records')
        # print(single_ps_df)
        
        cursor.close()
        db.close()
        return single_ps_df, single_gt_df

    except:
        return 'Error'


# get_single_domain('https://3waysdigital.com')

# def create_table():
#     cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(1000))")

# create_table()
# def new_user(username,password):
#     sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
#     values = (username, password)
#     cursor.execute(sql, values)
#     db.commit()


# def get_user(username):
#     sql = "SELECT * FROM users WHERE username = %s"
#     values = (username,)
#     cursor.execute(sql, values)

#     result = cursor.fetchall()
#     if result == []:
#         return None
#     else:
#         for user in result:
#             return user[2]

def get_all():
    try:
        db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB
        )
        # cursor = db.cursor()

        ps_df = pd.read_sql_query(f"SELECT * FROM google_page_speed;",con=db)
        ps_df['measurement_date'] = pd.to_datetime(ps_df['measurement_date']).dt.date.astype(str)

        gt_df = pd.read_sql_query(f"SELECT * FROM gtmetrix;",con=db)
        gt_df['measurement_date'] = pd.to_datetime(gt_df['measurement_date']).dt.date.astype(str)

        ps_df = ps_df.to_dict(orient='records')
        gt_df = gt_df.to_dict(orient='records')
        # print(ps_df)
        # print(type(ps_df))
        response = {'pagespeed': ps_df, 'gtmetrix': gt_df}
        # cursor.close()
        db.close()

        return response
    except DatabaseError as e:

        return 'Error'


# get_all()
# def get_entries_count():
#     sql = 'SELECT COUNT(id) from google_page_speed UNION SELECT COUNT(id) from gtmetrix'
#     cursor.execute(sql,)
#     result = cursor.fetchall()
#     return result[0][0] 


def get_basic_metrics():
    db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB
    )
    cursor = db.cursor()
    sql = 'SELECT COUNT(id) from google_page_speed UNION SELECT COUNT(id) from gtmetrix'
    cursor.execute(sql,)
    result = cursor.fetchall()
    count= result[0][0]

    ps_df = pd.read_sql_query(f"SELECT * FROM google_page_speed;",con=db)
    ps_df['measurement_date'] = pd.to_datetime(ps_df['measurement_date']).dt.date.astype(str)

    gt_df = pd.read_sql_query(f"SELECT * FROM gtmetrix;",con=db)
    gt_df['measurement_date'] = pd.to_datetime(gt_df['measurement_date']).dt.date.astype(str)

    ps_means = ps_df.mean().to_dict()
    gt_means = gt_df.mean().to_dict()

    gt_grade_counts = gt_df['gtmetrix_grade'].value_counts().to_dict()

    top25_ps = ps_df[ps_df['performance'].ge(ps_df['performance'].quantile(q=.75))]
    top25_gt =gt_df[gt_df['performance_score'].ge(gt_df['performance_score'].quantile(q=.75))]

    bottom25_ps = ps_df[ps_df['performance'].le(ps_df['performance'].quantile(q=.25))]
    bottom25_gt =gt_df[gt_df['performance_score'].le(gt_df['performance_score'].quantile(q=.25))]

    stats = {
        'total_entries_count': count,
        'gtmetrix_means': gt_means,
        'pagespeed_means': ps_means,
        'gtmetrix_grade_counts': gt_grade_counts,
        'top_25_gtmetrix': top25_gt.to_dict(orient='records'),
        'top_25_pagespeed': top25_ps.to_dict(orient='records'),
        'bottom_25_gtmetrix': bottom25_gt.to_dict(orient='records'),
        'bottom_25_pagespeed':bottom25_ps.to_dict(orient='records')
    }
    # print(stats)
    cursor.close()
    db.close()


    return stats

# get_basic_metrics()

def get_na():
    db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB
    )
    # cursor = db.cursor()
    ps_df = pd.read_sql_query(f"SELECT * FROM google_page_speed;",con=db)
    ps_df['measurement_date'] = pd.to_datetime(ps_df['measurement_date']).dt.date.astype(str)

    gt_df = pd.read_sql_query(f"SELECT * FROM gtmetrix;",con=db)
    gt_df['measurement_date'] = pd.to_datetime(gt_df['measurement_date']).dt.date.astype(str)

    df = gt_df.merge(ps_df, left_index=True, right_index=True)
    df_na = df[df.isnull().any(axis=1)]

    df_na = df_na.to_dict(orient='records')
    # cursor.close()
    db.close()

    return df_na

def add_domain(domain,server):
    db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB
    )
    cursor = db.cursor()

    sql = "INSERT INTO domains (domain, mosaic_server) VALUES (%s, %s)"
    val = (domain, server)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


# get_na()
# get_entries_count()
# get_all()
# get_user('majormajor2')










