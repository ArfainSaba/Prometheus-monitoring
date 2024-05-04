# services.py

queries = {
    "get_datasets": "SELECT * FROM datasets;",
    "get_item": "SELECT * FROM datasets WHERE id = %s;",
    "create_dataset": """
        INSERT INTO datasets (id, dataset_id, type, name, validation_config, extraction_config, dedup_config, 
                              data_schema, denorm_config, router_config, dataset_config, status, tags, data_version, 
                              created_by, updated_by, created_date, updated_date, published_date)
        VALUES (%(id)s, %(dataset_id)s, %(type)s, %(name)s, %(validation_config)s, %(extraction_config)s, 
                %(dedup_config)s, %(data_schema)s, %(denorm_config)s, %(router_config)s, %(dataset_config)s, 
                %(status)s, %(tags)s, %(data_version)s, %(created_by)s, %(updated_by)s, %(created_date)s, 
                %(updated_date)s, %(published_date)s);
    """,
    "update_dataset": """
        UPDATE datasets 
        SET 
            dataset_id = %(dataset_id)s, 
            type = %(type)s, 
            name = %(name)s, 
            validation_config = %(validation_config)s, 
            extraction_config = %(extraction_config)s, 
            dedup_config = %(dedup_config)s, 
            data_schema = %(data_schema)s, 
            denorm_config = %(denorm_config)s, 
            router_config = %(router_config)s, 
            dataset_config = %(dataset_config)s, 
            status = %(status)s, 
            tags = %(tags)s, 
            data_version = %(data_version)s, 
            created_by = %(created_by)s, 
            updated_by = %(updated_by)s, 
            created_date = %(created_date)s, 
            updated_date = %(updated_date)s, 
            published_date = %(published_date)s
        WHERE 
            id = %(id)s;
    """,
    "delete_dataset": "DELETE FROM datasets WHERE id = %s;"
}
