from flask import Flask, jsonify, request
from flask import Response
from werkzeug.exceptions import BadRequestKeyError
from ecom_meta_ads import MetaAdsEcomru
from flasgger import Swagger, swag_from
from config import Configuration
from get_token import get_token
import logger
from db_work import put_query
from sqlalchemy import create_engine
import os

# токен для отладки
# user_token = 'EAAi2zWytf0wBACKJIOUTHHfi2yPYXBGav1TDziJXWwMPv9hdZBd9J4jilcr2UWXyEp9F3n9ZB2k4hXW3wQdHuYXa0ZBy9esRc96BM3CZCjTqPNVxjYU9uKr0yqrgHwv5s9F9bVTAgELxFMz0Q0uIq13UvipYuinIVCrE6w4PLAZDZD'

logger = logger.init_logger()

app_id = os.environ.get('META_APP_ID', None)
app_secret = os.environ.get('META_APP_SECRET', None)
# app_id = 2452793221545804
# app_secret = '514f367353ac4712b328c12537b485fa'
# redirect_uri = 'https://www.facebook.com'
redirect_uri = 'https://developers.facebook.com'

host = os.environ.get('ECOMRU_PG_HOST', None)
port = os.environ.get('ECOMRU_PG_PORT', None)
ssl_mode = os.environ.get('ECOMRU_PG_SSL_MODE', None)
db_name = os.environ.get('ECOMRU_PG_DB_NAME', None)
user = os.environ.get('ECOMRU_PG_USER', None)
password = os.environ.get('ECOMRU_PG_PASSWORD', None)
target_session_attrs = 'read-write'

# host = 'localhost'
# port = '5432'
# db_name = 'postgres'
# user = 'postgres'
# password = ' '

db_params = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(db_params)


app = Flask(__name__)
app.config.from_object(Configuration)
app.config['SWAGGER'] = {"title": "Swagger-UI", "uiversion": 3}


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json()",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.route('/metamarketing/authlink', methods=['GET'])
@swag_from("swagger_conf/authlink.yml")
def get_authlink():
    """returns link for getting access token"""

    try:
        meta = MetaAdsEcomru(app_id=app_id, app_secret=app_secret, redirect_uri=redirect_uri)

        return jsonify({'link': meta.auth_url})

    except BadRequestKeyError:
        logger.error("authlink: BadRequest")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'authlink: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/getcampaigns', methods=['POST'])
@swag_from("swagger_conf/get_campaigns.yml")
def get_campaigns():
    """returns campaigns"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        return jsonify(meta.get_campaigns(status='all').json())

    except BadRequestKeyError:
        logger.error("get campaigns: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get campaigns: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get campaigns: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/getadsets', methods=['POST'])
@swag_from("swagger_conf/get_adsets.yml")
def get_adsets():
    """return adsets"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        campaign_id = json_file.get("campaign_id", None)

        res = meta.get_adsets(campaign_id=campaign_id)

        if res.status_code == 200:
            logger.info(f"get adsets: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400:
            logger.info(f"get adsets: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"get adsets: marketing api error {res.status_code}")
            return jsonify({'error': 'marketing api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("get adsets: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get adsets: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get adsets: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/getads', methods=['POST'])
@swag_from("swagger_conf/get_ads.yml")
def get_ads():
    """return ads"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        campaign_id = json_file.get("campaign_id", None)
        adset_id = json_file.get("adset_id", None)

        res = meta.get_ads(campaign_id=campaign_id, adset_id=adset_id)

        if res.status_code == 200:
            logger.info(f"get ads: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400:
            logger.info(f"get ads: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"get ads: marketing api error {res.status_code}")
            return jsonify({'error': 'marketing api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("get ads: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get ads: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get ads: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/addcampaign', methods=['POST'])
@swag_from("swagger_conf/add_campaign.yml")
def add_campaign():
    """Add campaign"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        name = json_file["name"]
        objective = json_file.get("objective", None)
        status = json_file["status"]
        special_ad_categories = json_file.get("special_ad_categories", None)
        adlabels = json_file.get("adlabels", None)
        bid_strategy = json_file.get("bid_strategy", None)
        buying_type = json_file.get("buying_type", None)
        campaign_optimization_type = json_file.get("campaign_optimization_type", None)
        daily_budget = json_file.get("daily_budget", None)
        execution_options = json_file.get("execution_options", None)
        is_skadnetwork_attribution = json_file.get("is_skadnetwork_attribution", None)
        is_using_l3_schedule = json_file.get("is_using_l3_schedule", None)
        iterative_split_test_configs = json_file.get("iterative_split_test_configs", None)
        lifetime_budget = json_file.get("lifetime_budget", None)
        source_campaign_id = json_file.get("source_campaign_id", None)
        special_ad_category_country = json_file.get("special_ad_category_country", None)
        spend_cap = json_file.get("spend_cap", None)
        start_time = json_file.get("start_time", None)
        stop_time = json_file.get("stop_time", None)
        topline_id = json_file.get("topline_id", None)

        res = meta.add_campaign(name=name,
                                objective=objective,
                                status=status,
                                special_ad_categories=special_ad_categories,
                                adlabels=adlabels,
                                bid_strategy=bid_strategy,
                                buying_type=buying_type,
                                campaign_optimization_type=campaign_optimization_type,
                                daily_budget=daily_budget,
                                execution_options=execution_options,
                                is_skadnetwork_attribution=is_skadnetwork_attribution,
                                is_using_l3_schedule=is_using_l3_schedule,
                                iterative_split_test_configs=iterative_split_test_configs,
                                lifetime_budget=lifetime_budget,
                                source_campaign_id=source_campaign_id,
                                special_ad_category_country=special_ad_category_country,
                                spend_cap=spend_cap,
                                start_time=start_time,
                                stop_time=stop_time,
                                topline_id=topline_id)

        put_query(json_file=json_file, table_name='meta_add_campaigns', result=res, engine=engine, logger=logger)

        if res.status_code == 200:
            logger.info(f"add campaign: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400:
            logger.info(f"add campaign: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"add campaign: marketing api error {res.status_code}")
            return jsonify({'error': 'marketing api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add campaign: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add campaign: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add campaign: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/addadset', methods=['POST'])
@swag_from("swagger_conf/add_adset.yml")
def add_adset():
    """Add adset"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        # собираем таргетинг
        t_countries = json_file.get("t_countries", None)
        t_regions = json_file.get("t_regions", None)
        t_cities_keys = json_file.get("t_cities_keys", None)
        t_cities_rads = json_file.get("t_cities_rads", None)
        t_cities_dist_unit = json_file.get("t_cities_dist_unit", None)
        t_geo_markets_keys = json_file.get("t_geo_markets_keys", None)
        t_geo_markets_names = json_file.get("t_geo_markets_names", None)
        t_location_types = json_file.get("t_location_types", None)
        t_country_groups = json_file.get("t_country_groups", None)
        t_interests_ids = json_file.get("t_interests_ids", None)
        t_interests_names = json_file.get("t_interests_names", None)
        t_age_max = json_file.get("t_age_max", None)
        t_age_min = json_file.get("t_age_min", None)
        t_genders = json_file.get("t_genders", None)
        t_device_platforms = json_file.get("t_device_platforms", None)
        t_publisher_platforms = json_file.get("t_publisher_platforms", None)
        t_behaviors_ids = json_file.get("t_behaviors_ids", None)
        t_behaviors_names = json_file.get("t_behaviors_names", None)

        targeting = meta.targeting(t_countries=t_countries,
                                   t_regions=t_regions,
                                   t_cities_keys=t_cities_keys,
                                   t_cities_rads=t_cities_rads,
                                   t_cities_dist_unit=t_cities_dist_unit,
                                   t_geo_markets_keys=t_geo_markets_keys,
                                   t_geo_markets_names=t_geo_markets_names,
                                   t_location_types=t_location_types,
                                   t_country_groups=t_country_groups,
                                   t_interests_ids=t_interests_ids,
                                   t_interests_names=t_interests_names,
                                   t_age_max=t_age_max,
                                   t_age_min=t_age_min,
                                   t_genders=t_genders,
                                   t_device_platforms=t_device_platforms,
                                   t_publisher_platforms=t_publisher_platforms,
                                   t_behaviors_ids=t_behaviors_ids,
                                   t_behaviors_names=t_behaviors_names)

        if targeting is None:
            logger.error("add adset: targeting age params incorrect")
            return jsonify({'error': 'targeting age params incorrect'})
        else:
            name = json_file["name"]
            campaign_id = json_file["campaign_id"]
            optimization_goal = json_file["optimization_goal"]
            status = json_file["status"]
            bid_amount = json_file.get("bid_amount", None)
            bid_strategy = json_file.get("bid_strategy", None)
            billing_event = json_file.get("billing_event", None)
            daily_budget = json_file.get("daily_budget", None)
            lifetime_budget = json_file.get("lifetime_budget", None)
            start_time = json_file.get("start_time", None)
            end_time = json_file.get("end_time", None)
            adlabels = json_file.get("adlabels", None)
            adset_schedule_start_minutes = json_file.get("adset_schedule_start_minutes", None)
            adset_schedule_end_minutes = json_file.get("adset_schedule_end_minutes", None)
            adset_schedule_days = json_file.get("adset_schedule_days", None)
            adset_schedule_timezone_types = json_file.get("adset_schedule_timezone_types", None)
            attribution_spec_event_type = json_file.get("attribution_spec_event_type", None)
            attribution_spec_window_days = json_file.get("attribution_spec_window_days", None)
            contextual_bundling_spec_status = json_file.get("contextual_bundling_spec_status", None)
            creative_sequence = json_file.get("creative_sequence", None)
            daily_imps = json_file.get("daily_imps", None)
            daily_min_spend_target = json_file.get("daily_min_spend_target", None)
            daily_spend_cap = json_file.get("daily_spend_cap", None)
            destination_type = json_file.get("destination_type", None)
            execution_options = json_file.get("execution_options", None)
            existing_customer_budget_percentage = json_file.get("existing_customer_budget_percentage", None)
            frequency_control_specs_events = json_file.get("frequency_control_specs_events", None)
            frequency_control_specs_interval_days = json_file.get("frequency_control_specs_interval_days", None)
            frequency_control_specs_max_frequency = json_file.get("frequency_control_specs_max_frequency", None)
            is_dynamic_creative = json_file.get("is_dynamic_creative", None)
            lifetime_imps = json_file.get("lifetime_imps", None)
            lifetime_min_spend_target = json_file.get("lifetime_min_spend_target", None)
            lifetime_spend_cap = json_file.get("lifetime_spend_cap", None)
            multi_optimization_goal_weight = json_file.get("multi_optimization_goal_weight", None)
            optimization_sub_event = json_file.get("optimization_sub_event", None)
            pacing_type = json_file.get("pacing_type", None)
            promoted_object_pixel_id = json_file.get("promoted_object_pixel_id", None)
            promoted_object_custom_event_type = json_file.get("promoted_object_custom_event_type", None)
            promoted_object_pixel_rule = json_file.get("promoted_object_pixel_rule", None)
            promoted_object_event_id = json_file.get("promoted_object_event_id", None)
            promoted_object_application_id = json_file.get("promoted_object_application_id", None)
            promoted_object_object_store_url = json_file.get("promoted_object_object_store_url", None)
            promoted_object_offline_conversion_data_set_id = json_file.get("promoted_object_offline_conversion_data_set_id", None)
            promoted_object_page_id = json_file.get("promoted_object_page_id", None)
            promoted_object_custom_event_str = json_file.get("promoted_object_custom_event_str", None)
            promoted_object_product_set_id = json_file.get("promoted_object_product_set_id", None)
            promoted_object_offer_id = json_file.get("promoted_object_offer_id", None)
            promoted_object_product_item_id = json_file.get("promoted_object_product_item_id", None)
            promoted_object_instagram_profile_id = json_file.get("promoted_object_instagram_profile_id", None)
            promoted_object_fundraiser_campaign_id = json_file.get("promoted_object_fundraiser_campaign_id", None)
            promoted_object_mcme_conversion_id = json_file.get("promoted_object_mcme_conversion_id", None)
            rf_prediction_id = json_file.get("rf_prediction_id", None)
            time_based_ad_rotation_id_blocks = json_file.get("time_based_ad_rotation_id_blocks", None)
            time_based_ad_rotation_intervals = json_file.get("time_based_ad_rotation_intervals", None)
            time_start = json_file.get("time_start", None)
            time_stop = json_file.get("time_stop", None)
            tune_for_category = json_file.get("tune_for_category", None)

            res = meta.add_adset(name=name,
                                 campaign_id=campaign_id,
                                 optimization_goal=optimization_goal,
                                 targeting=targeting,
                                 status=status,
                                 bid_amount=bid_amount,
                                 bid_strategy=bid_strategy,
                                 billing_event=billing_event,
                                 daily_budget=daily_budget,
                                 lifetime_budget=lifetime_budget,
                                 start_time=start_time,
                                 end_time=end_time,
                                 adlabels=adlabels,
                                 adset_schedule_start_minutes=adset_schedule_start_minutes,
                                 adset_schedule_end_minutes=adset_schedule_end_minutes,
                                 adset_schedule_days=adset_schedule_days,
                                 adset_schedule_timezone_types=adset_schedule_timezone_types,
                                 attribution_spec_event_type=attribution_spec_event_type,
                                 attribution_spec_window_days=attribution_spec_window_days,
                                 contextual_bundling_spec_status=contextual_bundling_spec_status,
                                 creative_sequence=creative_sequence,
                                 daily_imps=daily_imps,
                                 daily_min_spend_target=daily_min_spend_target,
                                 daily_spend_cap=daily_spend_cap,
                                 destination_type=destination_type,
                                 execution_options=execution_options,
                                 existing_customer_budget_percentage=existing_customer_budget_percentage,
                                 frequency_control_specs_events=frequency_control_specs_events,
                                 frequency_control_specs_interval_days=frequency_control_specs_interval_days,
                                 frequency_control_specs_max_frequency=frequency_control_specs_max_frequency,
                                 is_dynamic_creative=is_dynamic_creative,
                                 lifetime_imps=lifetime_imps,
                                 lifetime_min_spend_target=lifetime_min_spend_target,
                                 lifetime_spend_cap=lifetime_spend_cap,
                                 multi_optimization_goal_weight=multi_optimization_goal_weight,
                                 optimization_sub_event=optimization_sub_event,
                                 pacing_type=pacing_type,
                                 promoted_object_pixel_id=promoted_object_pixel_id,
                                 promoted_object_custom_event_type=promoted_object_custom_event_type,
                                 promoted_object_pixel_rule=promoted_object_pixel_rule,
                                 promoted_object_event_id=promoted_object_event_id,
                                 promoted_object_application_id=promoted_object_application_id,
                                 promoted_object_object_store_url=promoted_object_object_store_url,
                                 promoted_object_offline_conversion_data_set_id=promoted_object_offline_conversion_data_set_id,
                                 promoted_object_page_id=promoted_object_page_id,
                                 promoted_object_custom_event_str=promoted_object_custom_event_str,
                                 promoted_object_product_set_id=promoted_object_product_set_id,
                                 promoted_object_offer_id=promoted_object_offer_id,
                                 promoted_object_product_item_id=promoted_object_product_item_id,
                                 promoted_object_instagram_profile_id=promoted_object_instagram_profile_id,
                                 promoted_object_fundraiser_campaign_id=promoted_object_fundraiser_campaign_id,
                                 promoted_object_mcme_conversion_id=promoted_object_mcme_conversion_id,
                                 rf_prediction_id=rf_prediction_id,
                                 time_based_ad_rotation_id_blocks=time_based_ad_rotation_id_blocks,
                                 time_based_ad_rotation_intervals=time_based_ad_rotation_intervals,
                                 time_start=time_start,
                                 time_stop=time_stop,
                                 tune_for_category=tune_for_category)

            put_query(json_file=json_file, table_name='meta_add_adsets', result=res, engine=engine, logger=logger)

            if res.status_code == 200:
                logger.info(f"add adset: {res.status_code}")
                return jsonify(res.json())
            elif res.status_code == 400:
                logger.info(f"add adset: {res.status_code}")
                return jsonify({'error': res.json(), 'status_code': res.status_code})
            else:
                logger.error(f"add adset: marketing api error {res.status_code}")
                return jsonify({'error': 'marketing api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add adset: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add adset: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add adset: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/metamarketing/addad', methods=['POST'])
@swag_from("swagger_conf/add_ad.yml")
def add_ad():
    """Add ad"""

    try:
        json_file = request.get_json(force=False)

        account_id = json_file["account_id"]
        user_token = get_token(account_id=account_id, json_file=json_file, engine=engine, logger=logger)

        meta = MetaAdsEcomru(ads_acc_id=account_id, user_token=user_token)

        name = json_file["name"]
        adset_id = json_file["adset_id"]
        creative_id = json_file["creative_id"]
        status = json_file["status"]
        adlabels = json_file.get("adlabels", None)
        audience_id = json_file.get("audience_id", None)
        bid_amount = json_file.get("bid_amount", None)
        conversion_domain = json_file.get("conversion_domain", None)
        date_format = json_file.get("date_format", None)
        display_sequence = json_file.get("display_sequence", None)
        draft_adgroup_id = json_file.get("draft_adgroup_id", None)
        engagement_audience = json_file.get("engagement_audience", None)
        execution_options = json_file.get("execution_options", None)
        include_demolink_hashes = json_file.get("include_demolink_hashes", None)
        priority = json_file.get("priority", None)
        source_ad_id = json_file.get("source_ad_id", None)

        res = meta.add_ad(name=name,
                          adset_id=adset_id,
                          creative_id=creative_id,
                          status=status,
                          adlabels=adlabels,
                          audience_id=audience_id,
                          bid_amount=bid_amount,
                          conversion_domain=conversion_domain,
                          date_format=date_format,
                          display_sequence=display_sequence,
                          draft_adgroup_id=draft_adgroup_id,
                          engagement_audience=engagement_audience,
                          execution_options=execution_options,
                          include_demolink_hashes=include_demolink_hashes,
                          priority=priority,
                          source_ad_id=source_ad_id)

        put_query(json_file=json_file, table_name='meta_add_ads', result=res, engine=engine, logger=logger)

        if res.status_code == 200:
            logger.info(f"add ad: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400 or res.status_code == 500:
            logger.info(f"add ad: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"add ad: marketing api error {res.status_code}")
            return jsonify({'error': 'marketing api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add ad: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add ad: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add ad: {ex}')
        raise HttpError(400, f'{ex}')



