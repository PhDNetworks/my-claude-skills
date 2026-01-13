#!/usr/bin/env python3
"""
Google Ads API Client for PhD Networks
Handles authentication and basic API operations.
"""

import json
import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration loading - from file or environment variables
# Config file path: ../../../google-ads-config.json (relative to repo root)
CONFIG_FILE_PATHS = [
    os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'google-ads-config.json'),
    os.path.expanduser('~/google-ads-config.json'),
    '/etc/google-ads-config.json'
]

def load_config() -> dict:
    """Load config from file or environment variables."""
    # Try config files first
    for path in CONFIG_FILE_PATHS:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)

    # Fall back to environment variables
    required_vars = ['GOOGLE_ADS_DEVELOPER_TOKEN', 'GOOGLE_ADS_CLIENT_ID',
                     'GOOGLE_ADS_CLIENT_SECRET', 'GOOGLE_ADS_REFRESH_TOKEN']

    if all(os.environ.get(var) for var in required_vars):
        return {
            "developer_token": os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.environ.get("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.environ.get("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "4906637401"),
            "use_proto_plus": True
        }

    raise FileNotFoundError(
        "Google Ads config not found. Create google-ads-config.json or set environment variables.\n"
        f"Searched paths: {CONFIG_FILE_PATHS}"
    )

# Lazy-load config when needed
DEFAULT_CONFIG = None


def get_client(config: dict = None) -> GoogleAdsClient:
    """Initialize and return a Google Ads API client."""
    global DEFAULT_CONFIG
    if config is None:
        if DEFAULT_CONFIG is None:
            DEFAULT_CONFIG = load_config()
        config = DEFAULT_CONFIG
    return GoogleAdsClient.load_from_dict(config)


def get_accessible_accounts(client: GoogleAdsClient, mcc_id: str = "4906637401") -> list:
    """Get all ENABLED client accounts under the MCC (excludes manager accounts)."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer_client.id,
            customer_client.descriptive_name,
            customer_client.status,
            customer_client.manager
        FROM customer_client
        WHERE customer_client.status = 'ENABLED'
            AND customer_client.manager = FALSE
    """

    accounts = []
    try:
        response = ga_service.search(customer_id=mcc_id, query=query)
        for row in response:
            accounts.append({
                "id": str(row.customer_client.id),
                "name": row.customer_client.descriptive_name
            })
    except GoogleAdsException as ex:
        print(f"Error fetching client accounts: {ex}")

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


# =============================================================================
# BUDGET MANAGEMENT FUNCTIONS
# =============================================================================

def get_campaign_budgets(client: GoogleAdsClient, customer_id: str, enabled_only: bool = False) -> list:
    """
    Get current budget settings for campaigns.

    Args:
        client: Google Ads API client
        customer_id: Customer ID (without dashes)
        enabled_only: If True, only return ENABLED campaigns (recommended for budget updates)
    """
    ga_service = client.get_service("GoogleAdsService")

    # Filter by ENABLED status if requested (important for budget updates)
    status_filter = "campaign.status = 'ENABLED'" if enabled_only else "campaign.status != 'REMOVED'"

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.id,
            campaign_budget.name,
            campaign_budget.amount_micros,
            campaign_budget.resource_name,
            campaign_budget.delivery_method,
            campaign_budget.status
        FROM campaign
        WHERE {status_filter}
    """

    budgets = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            budgets.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "campaign_status": row.campaign.status.name,
                "budget_id": row.campaign_budget.id,
                "budget_name": row.campaign_budget.name,
                "daily_budget": row.campaign_budget.amount_micros / 1_000_000,
                "daily_budget_micros": row.campaign_budget.amount_micros,
                "resource_name": row.campaign_budget.resource_name,
                "delivery_method": row.campaign_budget.delivery_method.name,
                "budget_status": row.campaign_budget.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error fetching budgets for {customer_id}: {ex}")

    return budgets


def update_campaign_budget(client: GoogleAdsClient, customer_id: str,
                          budget_resource_name: str, new_amount_micros: int) -> dict:
    """
    Update a campaign budget amount.

    Args:
        client: Google Ads API client
        customer_id: Customer ID (without dashes)
        budget_resource_name: Full resource name (customers/{id}/campaignBudgets/{budget_id})
        new_amount_micros: New daily budget in microcurrency (e.g., £8.00 = 8000000)

    Returns:
        dict with success status and details
    """
    from google.protobuf import field_mask_pb2

    campaign_budget_service = client.get_service("CampaignBudgetService")

    operation = client.get_type("CampaignBudgetOperation")
    budget = operation.update
    budget.resource_name = budget_resource_name
    budget.amount_micros = new_amount_micros

    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["amount_micros"]))

    try:
        response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[operation]
        )
        return {
            "success": True,
            "resource_name": response.results[0].resource_name,
            "new_amount": new_amount_micros / 1_000_000
        }
    except GoogleAdsException as ex:
        return {
            "success": False,
            "error": str(ex)
        }


def pause_campaign(client: GoogleAdsClient, customer_id: str, campaign_id: int) -> dict:
    """Pause a single campaign."""
    from google.protobuf import field_mask_pb2

    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[operation]
        )
        return {"success": True, "campaign_id": campaign_id, "status": "PAUSED"}
    except GoogleAdsException as ex:
        return {"success": False, "campaign_id": campaign_id, "error": str(ex)}


def enable_campaign(client: GoogleAdsClient, customer_id: str, campaign_id: int) -> dict:
    """Enable (un-pause) a single campaign."""
    from google.protobuf import field_mask_pb2

    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.status = client.enums.CampaignStatusEnum.ENABLED

    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[operation]
        )
        return {"success": True, "campaign_id": campaign_id, "status": "ENABLED"}
    except GoogleAdsException as ex:
        return {"success": False, "campaign_id": campaign_id, "error": str(ex)}


def pause_all_campaigns(client: GoogleAdsClient, customer_id: str) -> list:
    """Pause all ENABLED campaigns for an account. Returns list of results."""
    budgets = get_campaign_budgets(client, customer_id)
    results = []

    for b in budgets:
        if b["campaign_status"] == "ENABLED":
            result = pause_campaign(client, customer_id, b["campaign_id"])
            result["campaign_name"] = b["campaign_name"]
            results.append(result)

    return results


def enable_all_campaigns(client: GoogleAdsClient, customer_id: str, campaign_ids: list = None) -> list:
    """
    Enable campaigns for an account.

    Args:
        client: Google Ads API client
        customer_id: Customer ID
        campaign_ids: Optional list of specific campaign IDs to enable.
                     If None, enables all PAUSED campaigns.
    """
    results = []

    if campaign_ids is None:
        # Get all paused campaigns
        budgets = get_campaign_budgets(client, customer_id)
        campaign_ids = [b["campaign_id"] for b in budgets if b["campaign_status"] == "PAUSED"]

    for campaign_id in campaign_ids:
        result = enable_campaign(client, customer_id, campaign_id)
        results.append(result)

    return results


def get_account_spend_for_period(client: GoogleAdsClient, customer_id: str,
                                  start_date: str, end_date: str) -> float:
    """
    Get total spend for an account between two dates.

    Args:
        client: Google Ads API client
        customer_id: Customer ID
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Total spend in currency (not micros)
    """
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            metrics.cost_micros
        FROM customer
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    total_micros = 0
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            total_micros += row.metrics.cost_micros
    except GoogleAdsException as ex:
        print(f"Error fetching spend for {customer_id}: {ex}")

    return total_micros / 1_000_000


if __name__ == "__main__":
    # Test connection
    print("Testing Google Ads API connection...")
    print("Note: You need a valid refresh_token to connect.")
    print("\nTo generate a refresh token, run: python3 generate_refresh_token.py")
