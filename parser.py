import shutil

import logger
import os
import glob
import time
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from threading import Thread
from ecom_meta_ads import MetaAdsEcomru
from db_ecom_meta import DbMetaEcomru
import warnings
warnings.filterwarnings('ignore')

##################################
data_folder = './data'

delete_files = 1
upl_into_db = 1

breakdowns_types = [None, 'country', 'region',  'age,gender', 'publisher_platform,impression_device']

meta_table = 'meta_statistics'

##################################

logger = logger.init_logger()

# читаем параметры подключения
host = os.environ.get('ECOMRU_PG_HOST', None)
port = os.environ.get('ECOMRU_PG_PORT', None)
ssl_mode = os.environ.get('ECOMRU_PG_SSL_MODE', None)
db_name = os.environ.get('ECOMRU_PG_DB_NAME', None)
user = os.environ.get('ECOMRU_PG_USER', None)
password = os.environ.get('ECOMRU_PG_PASSWORD', None)
target_session_attrs = 'read-write'

# создаем рабочую папку, если еще не создана
if not os.path.isdir(data_folder):
    os.mkdir(data_folder)
# путь для сохранения файлов
path_ = f'{data_folder}/{str(date.today())}'
if not os.path.isdir(path_):
    os.mkdir(path_)


def get_reports(ads_acc_id, user_token):

    meta = MetaAdsEcomru(ads_acc_id=ads_acc_id, user_token=user_token)

    # получаем объявления
    # ads = meta.get_acc_ads()
    # ads_df = pd.DataFrame(ads.json()['data'])
    # ads_list = ads_df.id.values.tolist()
    # print(ads_list)

    ads_list = ['23851499996800328', '23851760787050328']

    # получаем последнюю дату
    last_date = database.get_last_date(account_id=ads_acc_id, table_name=meta_table)
    if last_date is not None:
        date_from = str(last_date + timedelta(days=1))
    else:
        date_from = str(date.today() - timedelta(days=30))

    date_to = str(date.today() - timedelta(days=1))

    reports_ids = []
    for ad_id in ads_list:
        for breakdown in breakdowns_types:
            insights = meta.get_insights(date_from, date_to,
                                         breakdowns=breakdown,
                                         campaign_id=None,
                                         adset_id=None,
                                         ad_id=ad_id,
                                         level=None,
                                         mode='async')

            reports_ids.append({'report_run_id': insights.json()['report_run_id'], 'breakdowns': breakdown})

    reports_df = pd.DataFrame(reports_ids)
    reports_df['breakdowns'] = reports_df['breakdowns'].str.replace(',', '')
    reports_df['breakdowns'] = reports_df['breakdowns'].str.replace('_', '-')

    for index_, keys_ in reports_df.iterrows():
        report_run_id = keys_[0]
        breakdowns = keys_[1]
        status = None
        # while status is None:
        #     status = meta.get_report_status(report_run_id).json()['data'][0]
        #     time.sleep(10)

        while status != 'Job Completed':
            status = meta.get_report_status(report_run_id).json()['async_status']
            print(f"{report_run_id}: {status}")
            logger.info(f"{report_run_id}: {status}")
            time.sleep(10)

        if not os.path.isdir(f'{path_}/{ads_acc_id}'):
            os.mkdir(f'{path_}/{ads_acc_id}')

        meta.export_reports(report_run_id,
                            name=report_run_id,
                            format='csv',
                            path=f"""{path_}/{ads_acc_id}/{report_run_id}_{breakdowns}.csv""")
        logger.info(f"""Saved - {path_}/{ads_acc_id}/{report_run_id}_{breakdowns}.csv""")


# создаем экземпляр класса, проверяем соединение с базой
database = DbMetaEcomru(host=host,
                        port=port,
                        ssl_mode=ssl_mode,
                        db_name=db_name,
                        user=user,
                        password=password,
                        target_session_attrs=target_session_attrs)

connection = database.test_db_connection()

if connection is not None:
    logger.info("connection to db - ok")

    # загружаем аккаунты
    # accounts = database.get_accounts().drop_duplicates(subset=['key_attribute_value', 'attribute_value'], keep='last')

    accs = [{
        'id': None,
        'key_attribute_value': 5675904092447021,
        'attribute_value': 'EAAMMcwxiN0ABAGhQ84qUw1KqlDTvyCU3nzJZB7kACozcyqKE2YrwoWeundPXeAEsmUyJfBFAZBZAlLY4awYARuW3uaA2ektO4A50IB6pCgo1WG8zhcxRHj4tTO8WJZBWm8vadCZBl6wAhqtAUbz99ZCq7sdyIiBOn94I2DE7A0wtZAX6C6ThN1DHGzZAstb8Gk9Jn3DQHMCwlQZDZD'
                 }]

    accounts = pd.DataFrame(accs)

    # создаем потоки
    threads = []
    for index, keys in accounts.iterrows():
        ads_acc_id = keys[1]
        user_token = keys[2]
        threads.append(Thread(target=get_reports, args=(ads_acc_id, user_token)))

    print(threads)

    # запускаем потоки
    for thread in threads:
        thread.start()

    # останавливаем потоки
    for thread in threads:
        thread.join()

else:
    logger.error('Error connection to db')
    print('Error connection to db')

# проверяем наличие загруженных файлов
files = []
for folder in os.listdir(path_):
    files += (glob.glob(os.path.join(f"{path_}/{folder}", "*.csv")))

if len(files) > 0:
    # создаем датасет на основе загруженных по API данных
    dataset = database.make_dataset(path=path_)
    print('dataset', dataset.shape)

    cols = dataset.columns.tolist()
    dataset = dataset.drop_duplicates(subset=cols, keep='first')
    print('dataset', dataset.shape)

    print(dataset)
    dataset.to_csv(f'{path_}/into_db.csv', sep=';', index=False)

    if upl_into_db == 1:
        upload = database.upl_to_db(dataset=dataset, table_name=meta_table)
        if upload is not None:
            logger.info("Upload to db successful")
        else:
            logger.error('Upload to db error')
    else:
        logger.info('Upl to db canceled')

else:
    logger.info("No files")
    print('No files')

if delete_files == 1:
    try:
        shutil.rmtree(path_)
        logger.info('Files (folder) deleted')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        logger.error('Error deleting')
else:
    print('Delete canceled')
    logger.info('Delete canceled')













