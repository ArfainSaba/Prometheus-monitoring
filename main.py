from psycopg2 import connect
import json
import time 
from prometheus_client import Counter, generate_latest, Gauge, Histogram
from services.services import queries
from fastapi import FastAPI, HTTPException,Response,Request
from models import datasetsModel
from typing import List
from prometheus_client.exposition import CONTENT_TYPE_LATEST
import uvicorn
import statistics 
import requests


conn_string = "host='db' port='5432' dbname='obsrv' user='obsrv_userr' password='obsrv123'"

print("connection successfull")


app = FastAPI()

api_requests_counter = Counter(
    "api_requests_total",
    "Total number of API calls",
    ["api", "status", "request_size", "response_size", "response_time"]
)

api_requests_gauge = Gauge(
    "api_response_time",
    "Total number of responses",
    ["api", "status", "request_size", "response_size", "response_time"]
)

# api_requests_counter.labels(status="200").inc()
# 4. Average response  time of all the API
    # 5. Average response time of successful API
    # 6. Average response time of failed API

conn = connect(conn_string)
cur= conn.cursor()
cur.execute("SELECT * FROM datasets;")
results=cur.fetchall()
cur.close()
conn.close()
response_times = []
successfull_response_time_array=[]
failed_response_time_Array=[]

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     # total_response_time.inc(process_time)
#     # total_response_time.set(process_time)
#     # successful_response_time.set(process_time)
#     # failed_response_time.set(process_time)
#     return response


@app.get('/')
async def root():
    return {"message": "success"}


@app.get("/metrics")
async def metrics():
    return Response(media_type="text/plain", content=generate_latest())


@app.get("/v1/dataset")
async def get_datasets() -> List[dict]:
    start_time = time.time()
    # total_api_calls.inc()
    
    # api_requests_counter.labels(status="200").inc()
    api_requests_counter.labels(api="app.get", status="", request_size="", response_size="", response_time="").inc()
    

    
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
        # successful_api_calls.inc()
        api_requests_counter.labels(api="app.get", status="200", request_size="", response_size="", response_time="").inc()
    
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.get", status="", request_size="", response_size="", response_time="").set(process_time * 1000)

        print("stuck")
        formatted_results.append(formatted_row)
        
    except:
        # failed_api_calls.inc()
        api_requests_counter.labels(api="app.get", status="404", request_size="", response_size="", response_time="").inc()
    
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.get", status="404", request_size="", response_size="", response_time="").set(process_time * 1000)


    finally:
        
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.get", status="", request_size="", response_size="", response_time="").set(process_time * 1000)

        
    return formatted_results



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
    start_time = time.time()
    print("inside post")
    # total_api_calls.inc()
    
    api_requests_counter.labels(api="app.post", status="", request_size="", response_size="", response_time="").inc()
    
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
        # successful_api_calls.inc()
        api_requests_counter.labels(api="app.post", status="200", request_size="", response_size="", response_time="").inc()
    
        cur.execute(queries["create_dataset"], datasetsmodel_dict)
        print("incremented")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Dataset created successfully"}
    except:
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_counter.labels(api="app.post", status="500", request_size="", response_size="", response_time="").inc()
    
        api_requests_gauge.labels(api="app.post", status="500", request_size="", response_size="", response_time="").set(process_time * 1000)

    finally:
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.post", status="", request_size="", response_size="", response_time="").set(process_time * 1000)

        
        # end_time = time.time()
        # process_time = end_time - start_time
        # response_times.append(process_time)
        # total_response_time.set(process_time)
        # minrst= min(response_times)
        # min_response_time.set(minrst)
        # maxrst= max(response_times)
        # max_response_time.set(maxrst)
        # avg_response = statistics.mean(response_times)
        # avg_response_time.set(avg_response)

    return {"This Data already exists"}
    
    
    

@app.patch("/v1/datasets/{item_id}")
async def update_dataset(item_id:str, datasetsmodel:datasetsModel):
    # total_api_calls.inc()
    start_time = time.time()
    api_requests_counter.labels(api="app.patch", status="", request_size="", response_size="", response_time="").inc()
    
    try:
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
        # successful_api_calls.inc()
        api_requests_counter.labels(api="app.patch", status="200", request_size="", response_size="", response_time="").inc()
    

        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.patch", status="200", request_size="", response_size="", response_time="").set(process_time * 1000)



        conn.commit()
        cur.close()
        conn.close()

    except:
        api_requests_counter.labels(api="app.patch", status="500", request_size="", response_size="", response_time="").inc()
    
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.patch", status="500", request_size="", response_size="", response_time="").set(process_time * 1000)


    finally:
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.patch", status="200", request_size="", response_size="", response_time="").set(process_time * 1000)



    return {"message": "Dataset updated successfully"}

@app.delete("/v1/datasets/{item_id}")
def delete_dataset(item_id: str):
    start_time = time.time()
    # total_api_calls.inc()
    api_requests_counter.labels(api="app.delete", status="", request_size="", response_size="", response_time="").inc()
    
    try:
        conn = connect(conn_string)
        cur = conn.cursor()

        cur.execute(queries["get_item"], (item_id,))
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

        cur.execute(queries["delete_dataset"], (item_id,))
        
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.delete", status="200", request_size="", response_size="", response_time="").set(process_time * 1000)

        conn.commit()

        cur.close()
        conn.close()

    except:
        api_requests_counter.labels(api="app.delete", status="500", request_size="", response_size="", response_time="").inc()
    
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.delete", status="500", request_size="", response_size="", response_time="").set(process_time * 1000)


    finally:
        end_time = time.time()
        process_time = end_time - start_time
        response_times.append(process_time)
        api_requests_gauge.labels(api="app.delete", status="", request_size="", response_size="", response_time="").set(process_time * 1000)

        # end_time = time.time()
        # process_time = end_time - start_time
        # response_times.append(process_time)
        # total_response_time.set(process_time)
        # minrst= min(response_times)
        # min_response_time.set(minrst)
        # maxrst= max(response_times)
        # max_response_time.set(maxrst)
        # avg_response = statistics.mean(response_times)
        # avg_response_time.set(avg_response)
    return {"message":"Dataset deleted"}

cur.close()
conn.close()




if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8001)
    # start_http_server(8001)


