from psycopg2 import connect
import json
import time 
from prometheus_client import Counter, generate_latest, Gauge, Histogram
from services.services import queries
from fastapi import FastAPI, HTTPException,Response,Request
from models import datasetsModel
from typing import List
import uvicorn 


conn_string = "host='db' port='5432' dbname='obsrv' user='obsrv_userr' password='obsrv123'"

print("connection successfull")


app = FastAPI()


total_api_calls = Counter('total_api_calls', 'Total number of API calls')
successful_api_calls = Counter('successful_api_calls', 'Total number of successful API calls')
failed_api_calls = Counter('failed_api_calls', 'Total number of failed API calls')
total_response_time = Gauge('total_response_time', 'Total response time of all API calls')
successful_response_time = Gauge('successful_response_time', 'Response time of successful API calls')
failed_response_time = Gauge('failed_response_time', 'Response time of failed API calls')
max_response_time = Gauge('max_response_time', 'Max response time of all API calls')
min_response_time = Gauge('min_response_time', 'Min response time of all API calls')


conn = connect(conn_string)
cur= conn.cursor()
cur.execute("SELECT * FROM datasets;")
results=cur.fetchall()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # total_response_time.inc(process_time)
    total_response_time.set(process_time)
    successful_response_time.set(process_time)
    failed_response_time.set(process_time)
    return response


@app.get('/')
async def root():
    return {"message": "success"}


@app.get("/metrics")
async def metrics():
    return Response(media_type="text/plain", content=generate_latest())

@app.get("/v1/dataset")
async def get_datasets() -> List[dict]:
    total_api_calls.inc()
    try:
        formatted_results = []
        for row in results:
            formatted_row = {
            "id": row[0],
            "dataset_id": row[1],
            "type": row[2],
            "name": row[3],
            "validation_config": row[4],
            "extraction_config": row[5],
            "dedup_config": row[6],
            "data_schema": row[7],
            "denorm_config": row[8],
            "router_config": row[9],
            "dataset_config": row[10],
            "status": row[11],
            "tags": row[12],
            "data_version": row[13],
            "created_by": row[14],
            "updated_by": row[15],
            "created_date": row[16],
            "updated_date": row[17],
            "published_date": row[18]
        }
        formatted_results.append(formatted_row)
        successful_api_calls.inc()
        
    except:
        failed_api_calls.inc()
    return formatted_results
    # return results



@app.get("/v1/datasets/{item_id}")
def get_item(item_id:str, description="id of the item"):
    conn = connect(conn_string)
    cur = conn.cursor()
    cur.execute(queries["get_item"], (item_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

@app.post("/v1/datasets")
async def create_item(datasetsmodel:datasetsModel):
    print("inside post")
    total_api_calls.inc()
    try:
        conn = connect(conn_string)
        cur = conn.cursor()

        datasetsmodel_dict= datasetsmodel.dict()
        datasetsmodel_dict['validation_config'] = json.dumps(datasetsmodel_dict['validation_config'])
        datasetsmodel_dict['extraction_config'] = json.dumps(datasetsmodel_dict['extraction_config'])
        datasetsmodel_dict['dedup_config'] = json.dumps(datasetsmodel_dict['dedup_config'])

        datasetsmodel_dict['data_schema'] = json.dumps(datasetsmodel_dict['data_schema'])
        datasetsmodel_dict['denorm_config'] = json.dumps(datasetsmodel_dict['denorm_config'])
        datasetsmodel_dict['router_config'] = json.dumps(datasetsmodel_dict['router_config'])
        datasetsmodel_dict['dataset_config'] = json.dumps(datasetsmodel_dict['dataset_config'])

        # print("Datasets Model Dictionary:", datasetsmodel_dict) 
        cur.execute(queries["create_dataset"], datasetsmodel_dict)
        successful_api_calls.inc()
        print("incremented")
        conn.commit()
        cur.close()
        conn.close()
    except:
        failed_api_calls.inc()
        return {"This Data already exists"}
    
    
    return {"message": "Dataset created successfully"}

@app.patch("/v1/datasets/{item_id}")
async def update_dataset(item_id:str, datasetsmodel:datasetsModel):
    conn=connect(conn_string)
    cur=conn.cursor()

    cur.execute(queries["get_item"], (item_id,))
    existing_dataset = cur.fetchone()
    if not existing_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    datasetsmodel_dict = datasetsmodel.dict()

    datasetsmodel_dict['validation_config'] = json.dumps(datasetsmodel_dict['validation_config'])
    datasetsmodel_dict['extraction_config'] = json.dumps(datasetsmodel_dict['extraction_config'])
    datasetsmodel_dict['dedup_config'] = json.dumps(datasetsmodel_dict['dedup_config'])
    datasetsmodel_dict['data_schema'] = json.dumps(datasetsmodel_dict['data_schema'])
    datasetsmodel_dict['denorm_config'] = json.dumps(datasetsmodel_dict['denorm_config'])
    datasetsmodel_dict['router_config'] = json.dumps(datasetsmodel_dict['router_config'])
    datasetsmodel_dict['dataset_config'] = json.dumps(datasetsmodel_dict['dataset_config'])

    cur.execute(queries["update_dataset"], datasetsmodel_dict)


    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Dataset updated successfully"}

@app.delete("/v1/datasets/{item_id}")
def delete_dataset(item_id: str):
    conn = connect(conn_string)
    cur = conn.cursor()

    cur.execute(queries["get_item"], (item_id,))
    result = cur.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    cur.execute(queries["delete_dataset"], (item_id,))
    conn.commit()

    cur.close()
    conn.close()
    return {"message":"Dataset deleted"}

cur.close()
conn.close()




if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8001)
    # start_http_server(8001)


