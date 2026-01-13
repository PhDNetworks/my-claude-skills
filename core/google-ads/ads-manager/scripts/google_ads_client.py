#!/usr/bin/env python3
"""
Google Ads API Client for PhD Networks
Handles authentication and basic API operations.
"""

import json
import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Default credentials - can be overridden via environment variables or config file
DEFAULT_CONFIG = {
    "developer_token": os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "QEbSx8y0DWbQPKeR635KDg"),
    "client_id": os.environ.get("GOOGLE_ADS_CLIENT_ID", "1093467682273-mbbq6mpeoegnnehnisahv3mcouqgoemg.apps.googleusercontent.com"),
    "client_secret": os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "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"),
    "refresh_token": os.environ.get("GOOGLE_ADS_REFRESH_TOKEN", ""),  # Must be generated
    "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "4906637401"),  # MCC ID without dashes
    "use_proto_plus": True
}


def get_client(config: dict = None) -> GoogleAdsClient:
    """Initialize and return a Google Ads API client."""
    cfg = config or DEFAULT_CONFIG
    return GoogleAdsClient.load_from_dict(cfg)


def get_accessible_accounts(client: GoogleAdsClient, mcc_id: str = "4906637401") -> list:
    """Get all accessible customer accounts under the MCC."""
    customer_service = client.get_service("CustomerService")
    accessible_customers = customer_service.list_accessible_customers()
    
    accounts = []
    for resource_name in accessible_customers.resource_names:
        customer_id = resource_name.split('/')[-1]
        accounts.append(customer_id)
    
    return accounts


def get_account_details(client: GoogleAdsClient, customer_id: str) -> dict:
    """Get basic details for a customer account."""
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.manager
        FROM customer
        LIMIT 1
    """
    
    response = ga_service.search(customer_id=customer_id, query=query)
    
    for row in response:
        return {
            "id": row.customer.id,
            "name": row.customer.descriptive_name,
            "currency": row.customer.currency_code,
            "timezone": row.customer.time_zone,
            "is_manager": row.customer.manager
        }
    return None


def get_campaign_performance(client: GoogleAdsClient, customer_id: str, days: int = 30) -> list:
    """Get campaign performance metrics for the last N days."""
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.average_cpc,
            metrics.ctr
        FROM campaign
        WHERE segments.date DURING LAST_{days}_DAYS
            AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """
    
    campaigns = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            campaigns.append({
                "id": row.campaign.id,
                "name": row.campaign.name,
                "status": row.campaign.status.name,
                "channel": row.campaign.advertising_channel_type.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,  # Convert to currency
                "conversions": row.metrics.conversions,
                "conversion_value": row.metrics.conversions_value,
                "avg_cpc": row.metrics.average_cpc / 1_000_000,
                "ctr": row.metrics.ctr * 100  # Convert to percentage
            })
    except GoogleAdsException as ex:
        print(f"Error fetching campaigns for {customer_id}: {ex}")
    
    return campaigns


def get_keyword_performance(client: GoogleAdsClient, customer_id: str, days: int = 30) -> list:
    """Get keyword performance metrics."""
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group_criterion.quality_info.quality_score,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.average_cpc,
            metrics.ctr
        FROM keyword_view
        WHERE segments.date DURING LAST_{days}_DAYS
            AND ad_group_criterion.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 100
    """
    
    keywords = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            keywords.append({
                "ad_group": row.ad_group.name,
                "keyword": row.ad_group_criterion.keyword.text,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "status": row.ad_group_criterion.status.name,
                "quality_score": row.ad_group_criterion.quality_info.quality_score,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "avg_cpc": row.metrics.average_cpc / 1_000_000,
                "ctr": row.metrics.ctr * 100
            })
    except GoogleAdsException as ex:
        print(f"Error fetching keywords for {customer_id}: {ex}")
    
    return keywords


def get_search_terms_report(client: GoogleAdsClient, customer_id: str, days: int = 30) -> list:
    """Get search terms report to identify new keyword opportunities."""
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{days}_DAYS
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """
    
    search_terms = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            search_terms.append({
                "search_term": row.search_term_view.search_term,
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions
            })
    except GoogleAdsException as ex:
        print(f"Error fetching search terms for {customer_id}: {ex}")
    
    return search_terms


if __name__ == "__main__":
    # Test connection
    print("Testing Google Ads API connection...")
    print("Note: You need a valid refresh_token to connect.")
    print("\nTo generate a refresh token, run: python3 generate_refresh_token.py")
