import pandas as pd
import numpy as np
# import psycopg2
from datetime import datetime
import time
import json


def put_query(engine,
              logger,
              json_file,
              table_name: str,
              attempts: int = 1,
              result=None
              ):
    """Загружает запрос в БД"""

    try:
        if result.status_code == 200:

            res_id = result.json()["id"]

            if res_id is not None:
                json_file.setdefault("res_id", res_id)

            res_success = result.json()["success"]

            if res_success is not None:
                json_file.setdefault("res_success", str(res_success))

        elif result.status_code == 400:

            res_error = result.json()["error"]

            if res_error is not None:
                json_file.setdefault("res_error", str(res_error))

        else:
            res_error = result.text

            if res_error is not None:
                json_file.setdefault("res_error", str(res_error))

    except KeyError:
        res_error = result.text

        if res_error is not None:
            json_file.setdefault("res_error", str(res_error))

    # print(json_file)

    dataset = pd.DataFrame([json_file])
    dataset['date_time'] = datetime.now()
    dataset.drop('user_token', axis=1, inplace=True, errors='ignore')

    if table_name == 'meta_add_adsets':
        try:
            dataset['adset_schedule_days'] = dataset['adset_schedule_days'].astype('str', copy=True, errors='ignore')
            dataset['time_based_ad_rotation_id_blocks'] = dataset['time_based_ad_rotation_id_blocks'].astype('str', copy=True, errors='ignore')

            # print(type(dataset['adset_schedule_days'][0]))
            # print(type(dataset['time_based_ad_rotation_id_blocks'][0]))

        except KeyError:
            pass

    with engine.begin() as connection:
        n = 0
        while n < attempts:
            try:
                res = dataset.to_sql(name=table_name, con=connection, if_exists='append', index=False)
                logger.info(f"Upload to {table_name} - ok")
                return 'ok'
            except BaseException as ex:
                logger.error(f"data to db: {ex}")
                time.sleep(3)
                n += 1
        logger.error("data to db error")
        return None

