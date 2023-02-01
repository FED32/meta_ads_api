import requests
import json
import pandas as pd
import numpy as np


class MetaAdsEcomru:
    def __init__(self,
                 ads_acc_id: int = None,
                 user_token: str = None,
                 app_id=None,
                 app_secret=None,
                 redirect_uri=None
                 ):
        """
        https://developers.facebook.com/docs/marketing-api/overview/authorization#permissions-and-features

        """

        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri

        self.ads_acc_id = ads_acc_id
        self.user_token = user_token

        if self.app_id is not None and self.app_secret is not None:
            # self.auth_url = f"https://www.facebook.com/v15.0/dialog/oauth?client_id={self.app_id}&redirect_uri={self.redirect_uri}/&scope=ads_management"
            self.auth_url = f"https://www.facebook.com/v15.0/dialog/oauth?response_type=token&display=popup&client_id={self.app_id}&redirect_uri={self.redirect_uri}%2Ftools%2Fexplorer%2Fcallback&auth_type=rerequest&scope=read_insights%2Cads_management%2Cads_read%2Cbusiness_management"
        else:
            self.auth_url = None

        self.fields = [
            'created_time',
            'account_id', 'account_name',
            'campaign_id', 'campaign_name',
            'adset_id', 'adset_name',
            'ad_id', 'ad_name',
            #           'country',
            'account_currency',
            'cpc', 'cpm', 'cpp', 'ctr', 'clicks', 'impressions', 'cost_per_conversion', 'conversions',
            'action_values', 'actions',
            'reach', 'frequency', 'full_view_impressions',
            'full_view_reach',
            'website_ctr', 'cost_per_action_type', 'spend', 'inline_link_clicks', 'inline_link_click_ctr',
            'location',
            'buying_type',
            'canvas_avg_view_percent',
            'canvas_avg_view_time',
            'catalog_segment_value',
            'conversion_rate_ranking',
            'conversion_values',
            'cost_per_inline_link_click',
            'cost_per_inline_post_engagement',
            'cost_per_outbound_click',
            'cost_per_unique_action_type',
            'cost_per_unique_click',
            'cost_per_unique_inline_link_click',
            'cost_per_unique_outbound_click',
            'dda_results',
            'engagement_rate_ranking',
            'inline_post_engagement',
            'objective',
            'optimization_goal',
            'outbound_clicks',
            'outbound_clicks_ctr',
            'purchase_roas',
            'qualifying_question_qualify_answer_rate',
            'quality_ranking',
            'social_spend'
        ]

    def get_campaigns(self, status: str = 'active'):
        """
        returns campaigns
        https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#Reading

        """

        url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/campaigns'

        fields = [
            'id', 'account_id', 'ad_strategy_group_id', 'ad_strategy_id', 'name', 'objective', 'effective_status',
            'adlabels', 'bid_strategy', 'boosted_object_id', 'brand_lift_studies', 'budget_rebalance_flag',
            'budget_remaining', 'buying_type', 'can_create_brand_lift_study', 'can_use_spend_cap', 'configured_status',
            'created_time', 'daily_budget', 'has_secondary_skadnetwork_reporting', 'is_skadnetwork_attribution',
            'issues_info', 'last_budget_toggling_time', 'lifetime_budget', 'pacing_type', 'primary_attribution',
            'promoted_object', 'smart_promotion_type', 'source_campaign', 'source_campaign_id', 'special_ad_categories',
            'special_ad_category', 'special_ad_category_country', 'spend_cap', 'start_time', 'status', 'stop_time',
            'topline_id', 'updated_time'
        ]

        headers = {
            # 'fields': "['name', 'objective', 'effective_status']",
            'fields': str(fields),
            'access_token': self.user_token
        }

        if status == 'active':
            headers.setdefault('effective_status', "['ACTIVE', 'PAUSED']")
        if status == 'all':
            headers.setdefault('effective_status', "['ACTIVE', 'PAUSED', 'ARCHIVED', 'IN_PROCESS', 'WITH_ISSUES']")
        # print(headers)
        return requests.get(url, headers)

    def get_adsets(self, campaign_id: int = None):
        """
        return adsets
        https://developers.facebook.com/docs/marketing-api/reference/ad-campaign#Reading
        """

        if campaign_id is None:
            url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/adsets'
        else:
            url = f'https://graph.facebook.com/v15.0/{campaign_id}/adsets'

        fields = [
            'id', 'name', 'account_id', 'adlabels', 'adset_schedule', 'asset_feed_id', 'attribution_spec',
            'bid_adjustments', 'bid_amount', 'bid_constraints', 'bid_info', 'bid_strategy', 'billing_event',
            'budget_remaining', 'campaign', 'campaign_attribution', 'campaign_id', 'configured_status',
            'contextual_bundling_spec', 'created_time', 'creative_sequence', 'daily_budget', 'daily_min_spend_target',
            'daily_spend_cap', 'destination_type', 'effective_status', 'end_time', 'frequency_control_specs',
            'instagram_actor_id', 'is_dynamic_creative', 'issues_info', 'learning_stage_info', 'lifetime_budget',
            'lifetime_imps', 'lifetime_min_spend_target', 'lifetime_spend_cap', 'multi_optimization_goal_weight',
            'optimization_goal', 'optimization_sub_event', 'pacing_type', 'promoted_object', 'recommendations',
            'recurring_budget_semantics', 'review_feedback', 'rf_prediction_id', 'source_adset', 'source_adset_id',
            'start_time', 'status', 'targeting', 'targeting_optimization_types', 'time_based_ad_rotation_id_blocks',
            'time_based_ad_rotation_intervals', 'updated_time', 'use_new_app_click'
        ]

        headers = {
            "fields": ','.join(fields),
            # "fields": "name,configured_status,effective_status,start_time,end_time",
            "access_token": self.user_token
        }
        return requests.get(url, headers)

    # def get_camp_adsets(self, campaign_id):
    #     """
    #     returns adsets by campaign_id
    #     https://developers.facebook.com/docs/marketing-api/reference/ad-campaign#Reading
    #     """
    #
    #     url = f'https://graph.facebook.com/v15.0/{campaign_id}/adsets'
    #     headers = {"fields": "name,configured_status,effective_status,start_time,end_time",
    #                "access_token": self.user_token}
    #     return requests.get(url, headers)

    def get_ads(self,
                campaign_id: int = None,
                adset_id: int = None
                ):
        """
        return ads
        https://developers.facebook.com/docs/marketing-api/reference/adgroup#Reading
        """

        if campaign_id is not None:
            url = f'https://graph.facebook.com/v15.0/{campaign_id}/ads'
        elif adset_id is not None:
            url = f'https://graph.facebook.com/v15.0/{adset_id}/ads'
        else:
            url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/ads'

        fields = [
            'id', 'name', 'account_id', 'ad_review_feedback', 'adlabels', 'adset', 'adset_id', 'bid_amount', 'campaign',
            'campaign_id', 'configured_status', 'conversion_domain', 'created_time', 'creative', 'effective_status',
            'issues_info', 'last_updated_by_app_id', 'preview_shareable_link', 'recommendations', 'source_ad',
            'source_ad_id', 'status', 'tracking_specs', 'updated_time'
        ]

        headers = {
            "fields": ','.join(fields),
            # "fields": "id,name,bid_amount,effective_status,updated_time",
            "access_token": self.user_token
        }

        return requests.get(url, headers)

    def get_acc_ads(self):
        """
        returns ads by ads_acc_id
        """

        url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/ads'
        headers = {"fields": "id,name,bid_amount,effective_status,updated_time",
                   "access_token": self.user_token}
        return requests.get(url, headers)

    def get_camp_ads(self, campaign_id):
        """
        returns ads by campaign_id
        """
        
        url = f'https://graph.facebook.com/v15.0/{campaign_id}/ads'
        headers = {"fields": "id,name,bid_amount,effective_status,updated_time",
                   "access_token": self.user_token}
        return requests.get(url, headers)

    def get_adset_ads(self, adset_id):
        """
        returns ads by adset_id
        """
        url = f'https://graph.facebook.com/v15.0/{adset_id}/ads'
        headers = {"fields": "id,name,bid_amount,effective_status,updated_time",
                   "access_token": self.user_token}
        return requests.get(url, headers)

    def get_acc_insights(self, date_from, date_to, breakdowns=None, mode='sync'):
        """
        returns insights
        """
        url = f"https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/insights"

        headers = {
            'time_range': f"""{{'since':'{date_from}','until':'{date_to}'}}""",
            'time_increment': '1',
            'fields': ','.join(self.fields),
            'access_token': self.user_token}

        if breakdowns is not None:
            headers.setdefault('breakdowns', breakdowns)

        if mode == 'sync':
            return requests.get(url, headers)
        elif mode == 'async':
            return requests.post(url, headers)

    def get_insights(self,
                     date_from,
                     date_to,
                     breakdowns=None,
                     campaign_id=None,
                     adset_id=None,
                     ad_id=None,
                     level=None,
                     mode='async'):
        """
        returns insights
        """
        if campaign_id is not None:
            url = f'https://graph.facebook.com/v15.0/{campaign_id}/insights'
        elif adset_id is not None:
            url = f"https://graph.facebook.com/v15.0/{adset_id}/insights"
        elif ad_id is not None:
            url = f'https://graph.facebook.com/v15.0/{ad_id}/insights'
        else:
            url = f"https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/insights"

        headers = {
            # 'use_unified_attribution_setting': 'false',
            'export_columns': f"{self.fields}",
            'time_range': f"""{{'since':'{date_from}','until':'{date_to}'}}""",
            'time_increment': '1',
            'fields': ','.join(self.fields),
            'access_token': self.user_token}

        if breakdowns is not None:
            headers.setdefault('breakdowns', breakdowns)

        if level is not None:
            headers.setdefault('level', level)

        if mode == 'sync':
            return requests.get(url, headers)
        elif mode == 'async':
            return requests.post(url, headers)

    def get_report_status(self, report_run_id):
        """
        returns status report
        """
        # url = f'https://graph.facebook.com/v15.0/{report_run_id}/insights'
        url = f'https://graph.facebook.com/v15.0/{report_run_id}'
        headers = {'access_token': self.user_token}
        return requests.get(url, headers)

    def export_reports(self, report_run_id, name, format='csv', path='./reports'):
        """Download report"""

        url = 'https://www.facebook.com/ads/ads_insights/export_report/'
        headers = {'report_run_id': report_run_id,
                   'name': name,
                   'format': format,
                   'access_token': self.user_token
                   }
        req = requests.get(url, headers)
        if req.status_code == 200:
            with open(path, 'wb') as file:
                file.write(req.content)
            print('Сохранен ', path)
        else:
            print(req.text)

    def add_campaign(self,
                     name: str,
                     objective: str = None,
                     status: str = "PAUSED",
                     special_ad_categories: list = None,
                     adlabels: list = None,
                     bid_strategy: str = None,
                     buying_type: str = None,
                     campaign_optimization_type: str = None,
                     daily_budget: int = None,
                     execution_options: str = None,
                     is_skadnetwork_attribution: str = None,
                     is_using_l3_schedule: str = None,
                     iterative_split_test_configs: list = None,
                     lifetime_budget: int = None,
                     # promoted_object=None,
                     source_campaign_id: int = None,
                     special_ad_category_country: list = None,
                     spend_cap: int = None,
                     start_time: str = None,
                     stop_time: str = None,
                     topline_id: int = None,
                     promoted_object_application_id: int = None,
                     promoted_object_pixel_id: int = None,
                     promoted_object_custom_event_type: str = None,
                     promoted_object_object_store_url: str = None,
                     promoted_object_offer_id: int = None,
                     promoted_object_page_id: int = None,
                     promoted_object_product_catalog_id: int = None,
                     promoted_object_product_item_id: int = None,
                     promoted_object_instagram_profile_id: int = None,
                     promoted_object_product_set_id: int = None,
                     promoted_object_event_id: int = None,
                     promoted_object_offline_conversion_data_set_id: int = None,
                     promoted_object_fundraiser_campaign_id: int = None,
                     promoted_object_custom_event_str: str = None,
                     promoted_object_mcme_conversion_id: int = None,
                     promoted_object_omnichannel_object_app: list = None,
                     promoted_object_omnichannel_object_pixel: list = None,
                     promoted_object_omnichannel_object_onsite: list = None,
                     # upstream_events=None,
                     ):
        """
        Добавляет кампанию
        https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#----------2
        """

        url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/campaigns'

        headers = {
            'name': name,
            # 'objective': objective,
            'status': status,
            'special_ad_categories': ','.join(special_ad_categories),
            'access_token': self.user_token
        }

        if objective is not None:
            headers.setdefault('objective', objective)

        if adlabels is not None:
            headers.setdefault('adlabels', ','.join(adlabels))

        if bid_strategy is not None:
            headers.setdefault('bid_strategy', bid_strategy)

        if buying_type is not None:
            headers.setdefault('buying_type', buying_type)

        if campaign_optimization_type is not None:
            headers.setdefault('campaign_optimization_type', campaign_optimization_type)

        if daily_budget is not None:
            headers.setdefault('daily_budget', str(daily_budget))

        if execution_options is not None:
            headers.setdefault('execution_options', execution_options)

        if is_skadnetwork_attribution is not None:
            headers.setdefault('is_skadnetwork_attribution', is_skadnetwork_attribution)

        if is_using_l3_schedule is not None:
            headers.setdefault('is_using_l3_schedule', is_using_l3_schedule)

        if iterative_split_test_configs is not None:
            headers.setdefault('iterative_split_test_configs', ','.join(iterative_split_test_configs))

        if lifetime_budget is not None:
            headers.setdefault('lifetime_budget', str(lifetime_budget))

        if source_campaign_id is not None:
            headers.setdefault('source_campaign_id', str(source_campaign_id))

        if special_ad_category_country is not None:
            headers.setdefault('special_ad_category_country',  ','.join(special_ad_category_country))

        if spend_cap is not None:
            headers.setdefault('spend_cap', str(spend_cap))

        if start_time is not None:
            headers.setdefault('start_time', start_time)

        if stop_time is not None:
            headers.setdefault('stop_time', stop_time)

        if topline_id is not None:
            headers.setdefault('topline_id', str(topline_id))

        promoted_object = dict()
        if promoted_object_application_id is not None:
            promoted_object.setdefault("application_id", promoted_object_application_id)

        if promoted_object_pixel_id is not None:
            promoted_object.setdefault("pixel_id", promoted_object_pixel_id)

        if promoted_object_custom_event_type is not None:
            promoted_object.setdefault("custom_event_type", promoted_object_custom_event_type)

        if promoted_object_object_store_url is not None:
            promoted_object.setdefault("store_url", promoted_object_object_store_url)

        if promoted_object_offer_id is not None:
            promoted_object.setdefault("offer_id", promoted_object_offer_id)

        if promoted_object_page_id is not None:
            promoted_object.setdefault("page_id", promoted_object_page_id)

        if promoted_object_product_catalog_id is not None:
            promoted_object.setdefault("product_catalog_id", promoted_object_product_catalog_id)

        if promoted_object_product_item_id is not None:
            promoted_object.setdefault("product_item_id", promoted_object_product_item_id)

        if promoted_object_instagram_profile_id is not None:
            promoted_object.setdefault("instagram_profile_id", promoted_object_instagram_profile_id)

        if promoted_object_product_set_id is not None:
            promoted_object.setdefault("product_set_id", promoted_object_product_set_id)

        if promoted_object_event_id is not None:
            promoted_object.setdefault("event_id", promoted_object_event_id)

        if promoted_object_offline_conversion_data_set_id is not None:
            promoted_object.setdefault("offline_conversion_data_set_id", promoted_object_offline_conversion_data_set_id)

        if promoted_object_fundraiser_campaign_id is not None:
            promoted_object.setdefault("fundraiser_campaign_id", promoted_object_fundraiser_campaign_id)

        if promoted_object_custom_event_str is not None:
            promoted_object.setdefault("custom_event_str", promoted_object_custom_event_str)

        if promoted_object_mcme_conversion_id is not None:
            promoted_object.setdefault("mcme_conversion_id", promoted_object_mcme_conversion_id)

        if promoted_object_omnichannel_object_app is not None:
            promoted_object.setdefault("omnichannel_object")
            promoted_object["omnichannel_object"].setdefault("app", promoted_object_omnichannel_object_app)
        if promoted_object_omnichannel_object_pixel is not None:
            promoted_object.setdefault("omnichannel_object")
            promoted_object["omnichannel_object"].setdefault("pixel", promoted_object_omnichannel_object_pixel)
        if promoted_object_omnichannel_object_onsite is not None:
            promoted_object.setdefault("omnichannel_object")
            promoted_object["omnichannel_object"].setdefault("onsite", promoted_object_omnichannel_object_onsite)

        if len(promoted_object) > 0:
            headers.setdefault("promoted_object", str(promoted_object))

        return requests.post(url, headers)

    @staticmethod
    def targeting(t_countries: list = None,
                  t_regions: list = None,
                  t_cities_keys: list = None,
                  t_cities_rads: list = None,
                  t_cities_dist_unit="km",
                  t_geo_markets_keys: list = None,
                  t_geo_markets_names: list = None,
                  t_location_types: list = None,
                  t_country_groups: list = None,
                  t_interests_ids: list = None,
                  t_interests_names: list = None,
                  t_age_max: int = None,
                  t_age_min: int = None,
                  t_genders: int = None,
                  t_device_platforms: list = None,
                  t_publisher_platforms: list = None,
                  t_behaviors_ids: list = None,
                  t_behaviors_names: list = None
                  ):
        """
        Возвращает параметры таргетинга
        https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting

        https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting#demographics
        """

        result = dict()

        # age
        if t_age_min is not None:
            if t_age_min < 13:
                print("incorrect t_age_min")
                return None
            else:
                result.setdefault("age_min", t_age_min)
        if t_age_max is not None:
            if t_age_max > 65:
                print("incorrect t_age_max")
                return None
            result.setdefault("age_max", t_age_max)

        # genders
        if t_genders is not None:
            result.setdefault("genders", [t_genders])

        # geo_locations
        if t_countries is not None:
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("countries", t_countries)

        if t_regions is not None:
            regs = [{'key': id_} for id_ in t_regions]
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("regions", regs)

        if t_cities_keys is not None and t_cities_rads is not None:
            cities = [{'key': key, 'radius': rad, 'distance_unit': t_cities_dist_unit} for key, rad in zip(t_cities_keys, t_cities_rads)]
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("cities", cities)

        if t_geo_markets_keys is not None and t_geo_markets_names is not None:
            geo_markets = [{'key': key, 'name': name} for key, name in zip(t_geo_markets_keys, t_geo_markets_names)]
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("geo_markets", geo_markets)

        if t_location_types is not None:
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("location_types", t_location_types)

        if t_country_groups is not None:
            result.setdefault("geo_locations", {})
            result["geo_locations"].setdefault("country_groups", t_country_groups)

        # interests
        if t_interests_ids is not None and t_interests_names is None:
            interests = [{'id': id_} for id_ in t_interests_ids]
            result.setdefault("interests", interests)
        elif t_interests_ids is not None and t_interests_names is not None:
            interests = [{'id': id_, 'name': name} for id_, name in zip(t_interests_ids, t_interests_names)]
            result.setdefault("interests", interests)

        # device_platforms
        if t_device_platforms is not None:
            result.setdefault("device_platforms", t_device_platforms)

        # publisher_platforms
        if t_publisher_platforms is not None:
            result.setdefault("publisher_platforms", t_publisher_platforms)

        # behaviors
        if t_behaviors_ids is not None and t_behaviors_names is None:
            behaviors = [{'id': id_} for id_, name in t_behaviors_ids]
            result.setdefault("behaviors", behaviors)
        elif t_behaviors_ids is not None and t_behaviors_names is not None:
            behaviors = [{'id': id_, 'name': name} for id_, name in zip(t_behaviors_ids, t_behaviors_names)]
            result.setdefault("behaviors", behaviors)

        return result

    def add_adset(self,
                  name: str,
                  campaign_id: int,
                  optimization_goal: str,
                  targeting: dict,
                  status: str = "PAUSED",
                  bid_amount: int = None,
                  bid_strategy: str = None,
                  billing_event: str = None,
                  daily_budget: int = None,
                  lifetime_budget: int = None,
                  start_time: str = None,
                  end_time: str = None,
                  adlabels: list = None,
                  adset_schedule_start_minutes: list = None,
                  adset_schedule_end_minutes: list = None,
                  adset_schedule_days: list = None,
                  adset_schedule_timezone_types: list = None,
                  attribution_spec_event_type: list = None,
                  attribution_spec_window_days: list = None,
                  contextual_bundling_spec_status: str = None,
                  creative_sequence: list = None,
                  daily_imps: int = None,
                  daily_min_spend_target: int = None,
                  daily_spend_cap: int = None,
                  destination_type: str = None,
                  execution_options: list = None,
                  existing_customer_budget_percentage: int = None,
                  frequency_control_specs_events: list = None,
                  frequency_control_specs_interval_days: list = None,
                  frequency_control_specs_max_frequency: list = None,
                  is_dynamic_creative: str = None,
                  lifetime_imps: int = None,
                  lifetime_min_spend_target: int = None,
                  lifetime_spend_cap: int = None,
                  multi_optimization_goal_weight: str = None,
                  optimization_sub_event: str = None,
                  pacing_type: list = None,
                  promoted_object_pixel_id: int = None,
                  promoted_object_custom_event_type: str = None,
                  promoted_object_pixel_rule: int = None,
                  promoted_object_event_id: int = None,
                  promoted_object_application_id: int = None,
                  promoted_object_object_store_url: str = None,
                  promoted_object_offline_conversion_data_set_id: int = None,
                  promoted_object_page_id: int = None,
                  promoted_object_custom_event_str: str = None,
                  promoted_object_product_set_id: int = None,
                  promoted_object_offer_id: int = None,
                  promoted_object_product_item_id: int = None,
                  promoted_object_instagram_profile_id: int = None,
                  promoted_object_fundraiser_campaign_id: int = None,
                  promoted_object_mcme_conversion_id: int = None,
                  rf_prediction_id: int = None,
                  time_based_ad_rotation_id_blocks: list = None,
                  time_based_ad_rotation_intervals: list = None,
                  time_start: str = None,
                  time_stop: str = None,
                  tune_for_category: str = None
                  ):
        """
        Добавляет группу объявлений
        https://developers.facebook.com/docs/marketing-api/reference/ad-campaign

        """

        url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/adsets'

        headers = {
            'campaign_id': str(campaign_id),
            'name': name,
            'optimization_goal': optimization_goal,
            'status': status,
            'targeting': targeting,
            'start_time': start_time,
            'end_time': end_time,
            'access_token': self.user_token
        }

        if bid_amount is not None:
            headers.setdefault('bid_amount', str(bid_amount))

        if bid_strategy is not None:
            headers.setdefault('bid_strategy', bid_strategy)

        if billing_event is not None:
            headers.setdefault('billing_event', billing_event)

        if daily_budget is not None:
            headers.setdefault('daily_budget', str(daily_budget))

        if lifetime_budget is not None:
            headers.setdefault('lifetime_budget', str(lifetime_budget))

        if start_time is not None:
            headers.setdefault('start_time', start_time)

        if end_time is not None:
            headers.setdefault('end_time', end_time)

        if adlabels is not None:
            headers.setdefault('adlabels', ','.join(adlabels))

        if adset_schedule_start_minutes is not None and adset_schedule_end_minutes is not None and adset_schedule_days is not None and adset_schedule_timezone_types is not None:
            # headers.setdefault('adset_schedule', ','.join([adset_schedule_start_minute,
            #                                                adset_schedule_end_minute,
            #                                                # ','.join(adset_schedule_days),
            #                                                adset_schedule_days,
            #                                                adset_schedule_timezone_type]))
            adset_schedule = [{'start_minute': a, 'end_minute': b, 'days': c, 'timezone_type': d}
                              for a, b, c, d in zip(adset_schedule_start_minutes, adset_schedule_end_minutes, adset_schedule_days, adset_schedule_timezone_types)]
            headers.setdefault('adset_schedule', str(adset_schedule))

        if attribution_spec_event_type is not None and attribution_spec_window_days is not None:
            attribution_spec = [{'event_type': a, 'window_days': b} for a, b in zip(attribution_spec_event_type, attribution_spec_window_days)]
            headers.setdefault('attribution_spec', str(attribution_spec))

        if contextual_bundling_spec_status is not None:
            headers.setdefault('contextual_bundling_spec', str({'status': contextual_bundling_spec_status}))

        if creative_sequence is not None:
            headers.setdefault('creative_sequence', str(creative_sequence))

        if daily_imps is not None:
            headers.setdefault('daily_imps', str(daily_imps))

        if daily_min_spend_target is not None:
            headers.setdefault('daily_min_spend_target', str(daily_min_spend_target))

        if daily_spend_cap is not None:
            headers.setdefault('daily_spend_cap', str(daily_spend_cap))

        if destination_type is not None:
            headers.setdefault('destination_type', destination_type)

        if execution_options is not None:
            headers.setdefault('execution_options', ','.join(execution_options))

        if existing_customer_budget_percentage is not None:
            headers.setdefault('existing_customer_budget_percentage', str(existing_customer_budget_percentage))

        if frequency_control_specs_events is not None and frequency_control_specs_interval_days is not None and frequency_control_specs_max_frequency is not None:
            frequency_control_specs = [{'event': a, 'interval_days': b, 'max_frequency': c} for a, b, c in zip(frequency_control_specs_events,
                                                                                                               frequency_control_specs_interval_days,
                                                                                                               frequency_control_specs_max_frequency)]
            headers.setdefault('frequency_control_specs', str(frequency_control_specs))

        if is_dynamic_creative is not None:
            headers.setdefault('is_dynamic_creative', is_dynamic_creative)

        if lifetime_imps is not None:
            headers.setdefault('lifetime_imps', str(lifetime_imps))

        if lifetime_min_spend_target is not None:
            headers.setdefault('lifetime_min_spend_target', str(lifetime_min_spend_target))

        if lifetime_spend_cap is not None:
            headers.setdefault('lifetime_spend_cap', str(lifetime_spend_cap))

        if multi_optimization_goal_weight is not None:
            headers.setdefault('multi_optimization_goal_weight', multi_optimization_goal_weight)

        if optimization_sub_event is not None:
            headers.setdefault('optimization_sub_event', optimization_sub_event)

        if pacing_type is not None:
            headers.setdefault('pacing_type', ','.join(pacing_type))

        if promoted_object_pixel_id is not None and promoted_object_pixel_rule is None and promoted_object_custom_event_type is None:
            headers.setdefault('promoted_object', str({'pixel_id': promoted_object_pixel_id}))
        elif promoted_object_pixel_id is not None and promoted_object_pixel_rule is None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'pixel_id': promoted_object_pixel_id, 'custom_event_type': promoted_object_custom_event_type}))
        elif promoted_object_pixel_id is not None and promoted_object_pixel_rule is not None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'pixel_id': promoted_object_pixel_id, 'custom_event_type': promoted_object_custom_event_type, 'pixel_rule': promoted_object_pixel_rule}))
        elif promoted_object_event_id is not None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'event_id': promoted_object_event_id, 'custom_event_type': promoted_object_custom_event_type}))
        elif promoted_object_application_id is not None and promoted_object_object_store_url is not None and promoted_object_custom_event_type is not None:
            promoted_object = {'application_id': promoted_object_application_id, 'object_store_url': promoted_object_object_store_url, 'custom_event_type':  promoted_object_custom_event_type}
            if promoted_object_custom_event_str is not None:
                promoted_object.setdefault('custom_event_str', promoted_object_custom_event_str)
            headers.setdefault('promoted_object', str(promoted_object))
        elif promoted_object_application_id is not None and promoted_object_object_store_url is None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'application_id': promoted_object_application_id, 'custom_event_type': promoted_object_custom_event_type}))
        elif promoted_object_application_id is not None and promoted_object_object_store_url is not None and promoted_object_custom_event_type is None:
            headers.setdefault('promoted_object', str({'application_id': promoted_object_application_id, 'object_store_url': promoted_object_object_store_url}))
        elif promoted_object_offline_conversion_data_set_id is not None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'offline_conversion_data_set_id': promoted_object_offline_conversion_data_set_id, 'custom_event_type': promoted_object_custom_event_type}))
        elif promoted_object_page_id is not None:
            headers.setdefault('promoted_object', str({'page_id': promoted_object_page_id}))
        elif promoted_object_product_set_id is not None and promoted_object_custom_event_type is None:
            headers.setdefault('promoted_object', str({'product_set_id': promoted_object_product_set_id}))
        elif promoted_object_product_set_id is not None and promoted_object_custom_event_type is not None:
            headers.setdefault('promoted_object', str({'product_set_id': promoted_object_product_set_id, 'custom_event_type': promoted_object_custom_event_type}))
        elif promoted_object_offer_id is not None:
            headers.setdefault('promoted_object', str({'offer_id': promoted_object_offer_id}))
        elif promoted_object_product_item_id is not None:
            headers.setdefault('promoted_object', str({'promoted_object_product_item_id': promoted_object_product_item_id}))
        elif promoted_object_instagram_profile_id is not None:
            headers.setdefault('promoted_object', str({'instagram_profile_id': promoted_object_instagram_profile_id}))
        elif promoted_object_fundraiser_campaign_id is not None:
            headers.setdefault('promoted_object', str({'fundraiser_campaign_id': promoted_object_fundraiser_campaign_id}))
        elif promoted_object_mcme_conversion_id is not None:
            headers.setdefault('promoted_object', str({'mcme_conversion_id': promoted_object_mcme_conversion_id}))

        if rf_prediction_id is not None:
            headers.setdefault('rf_prediction_id', str(rf_prediction_id))

        if time_based_ad_rotation_id_blocks is not None:
            headers.setdefault('time_based_ad_rotation_id_blocks', ','.join([str(i) for i in time_based_ad_rotation_id_blocks]))

        if time_based_ad_rotation_intervals is not None:
            headers.setdefault('time_based_ad_rotation_intervals', ','.join(time_based_ad_rotation_intervals))

        if time_start is not None:
            headers.setdefault('time_start', time_start)

        if time_stop is not None:
            headers.setdefault('time_stop', time_stop)

        if tune_for_category is not None:
            headers.setdefault('tune_for_category', tune_for_category)

        return requests.post(url, headers)

    def add_ad(self,
               name: str,
               adset_id: int,
               creative_id: int,
               status: str = "PAUSED",
               adlabels: list = None,
               audience_id: str = None,
               bid_amount: int = None,
               conversion_domain: str = None,
               date_format: str = None,
               display_sequence: int = None,
               draft_adgroup_id: int = None,
               engagement_audience: str = None,
               execution_options: list = None,
               include_demolink_hashes: str = None,
               priority: int = None,
               source_ad_id: int = None
               ):
        """
        Добавляет объявление

        https://developers.facebook.com/docs/marketing-api/reference/adgroup

        """

        url = f'https://graph.facebook.com/v15.0/act_{self.ads_acc_id}/ads'

        headers = {
            'name': name,
            'adset_id': adset_id,
            'creative': f"""{{"creative_id": {creative_id}}}""",
            'status': status,
            'access_token': self.user_token
        }

        if adlabels is not None:
            headers.setdefault('adlabels', ','.join(adlabels))

        if audience_id is not None:
            headers.setdefault('audience_id', audience_id)

        if bid_amount is not None:
            headers.setdefault('bid_amount', str(bid_amount))

        if conversion_domain is not None:
            headers.setdefault('conversion_domain', conversion_domain)

        # if creative_id is not None:
        #     headers.setdefault('creative', {})
        #     headers['creative'].setdefault('creative_id', str(creative_id))

        if date_format is not None:
            headers.setdefault('date_format', date_format)

        if display_sequence is not None:
            headers.setdefault('display_sequence', str(display_sequence))

        if draft_adgroup_id is not None:
            headers.setdefault('draft_adgroup_id', str(draft_adgroup_id))

        if engagement_audience is not None:
            headers.setdefault('engagement_audience', engagement_audience)

        if execution_options is not None:
            # headers.setdefault('execution_options', ','.join(execution_options))
            headers.setdefault('execution_options', str(execution_options))

        if include_demolink_hashes is not None:
            headers.setdefault('include_demolink_hashes', include_demolink_hashes)

        if priority is not None:
            headers.setdefault('priority', str(priority))

        if source_ad_id is not None:
            headers.setdefault('source_ad_id', str(source_ad_id))

        # print(headers)

        return requests.post(url, headers)
