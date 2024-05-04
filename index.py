# from psycopg2 import connect
# # import requests
# from fastapi import FastAPI,Path


# conn_string = "host='localhost' \
# dbname='obsrv' user='obsrv_user' \
# password='obsrv123'"


# app=FastAPI()


# # use connect function to establish the connection
# conn = connect(conn_string)


# cur= conn.cursor()
# cur.execute("SELECT * FROM datasets;")
# # cur.execute("SELECT * FROM public.datasets;")
# cur.execute("SELECT * FROM datasets;")
# results=cur.fetchall()
# # cur.close()
# # conn.close()




# # response= requests.get("http://127.0.0.1:8000/v1/dataset/{id}")
# # if(response.ok):
# #     data=response.json()
# #     id_to_query= data.get('id')






# #     cur.execute("SELECT * FROM public.datasets WHERE id = %s", (id_to_query,))
# # else:
# #     print("invalid id")

# @app.get("/v1/datasets/{item_id}")
# def get_item(item_id:int, description="id of the item"):
#     conn = connect(conn_string)
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM datasets WHERE id = %s", (item_id,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return result
#     # return results[item_id]
 


# # results=cur.fetchall()




# cur.close()
# conn.close()


# for row in results:
#     print(row)
