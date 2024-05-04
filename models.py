from fastapi import FastAPI
from pydantic import BaseModel
# from sqlalchemy import Column
# from sqlalchemy import String,Integer,TIMESTAMP,func, Boolean
# from sqlalchemy.dialects.postgresql import JSON, ARRAY
from datetime import datetime
from typing import Optional,List


class ValidationConfig(BaseModel):
    validate: bool
    mode: str
    validation_mode: str

class ExtractionConfig(BaseModel):
    is_batch_event: bool
    extraction_key: str

class DedupConfig(BaseModel):
    drop_duplicates: bool
    dedup_key: str
    dedup_period: int

class DataSchema(BaseModel):
    schema: str  # Adjust the type according to your actual schema definition

class DenormConfig(BaseModel):
    redis_db_host: str
    redis_db_port: int
    denorm_fields: List[dict]  # Adjust the type according to your actual denormalization config

class RouterConfig(BaseModel):
    topic: str

class DatasetConfig(BaseModel):
    data_key: str
    timestamp_key: str
    exclude_fields: List[str]
    entry_topic: str
    redis_db_host: str
    redis_db_port: int
    index_data: bool
    redis_db: int



class datasetsModel(BaseModel):
    id: str
    dataset_id: str
    type: str
    name: str
    validation_config: ValidationConfig
    extraction_config: ExtractionConfig
    dedup_config: DedupConfig
    data_schema: DataSchema
    denorm_config: DenormConfig
    router_config: RouterConfig
    dataset_config: DatasetConfig
    status: str
    tags: Optional[List[str]] = []
    data_version: int
    created_by: str
    updated_by: str
    created_date: datetime
    updated_date: datetime
    published_date: datetime

# class DatasetResponse():
#     id: 
#     stat
#     body: 