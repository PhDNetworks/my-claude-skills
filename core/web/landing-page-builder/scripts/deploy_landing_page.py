#!/usr/bin/env python3
"""
Landing Page Deployment Orchestrator

Deploys high-converting, Core Web Vitals-optimized landing pages
to WordPress sites via SSH/WP-CLI.

Usage:
    python deploy_landing_page.py --site jlr_smith_roofing --keyword "roof repairs leeds"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Local imports
from wp_cli_commands import WordPressClient
from schema_generator import generate_local_business_schema
from conversion_tracking import setup_ga4_tracking

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"


def load_site_config(site_name: str) -> dict:
    """Load site configuration from JSON file."""
    config_path = CONFIG_DIR / "site_configs" / f"{site_name}.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Site config not found: {config_path}")

    with open(config_path) as f:
        return json.load(f)


def generate_page_content(keyword: str, site_config: dict) -> dict:
    """Generate optimized page content from keyword and site config."""

    # Extract location from keyword or use site default
    location = site_config.get("location", "Leeds")
    business_name = site_config.get("business_name", "")
    phone = site_config.get("phone", "")

    # Generate H1 (must contain keyword)
    h1 = keyword.title()
    if location.lower() not in keyword.lower():
        h1 = f"{keyword.title()} in {location}"

    # Generate meta title (60 chars max)
    meta_title = f"{h1} | Free Quote | {business_name}"[:60]

    # Generate meta description (155 chars max)
    meta_description = f"Professional {keyword} services in {location}. " \
                       f"Free quotes, fully insured, local experts. " \
                       f"Call {phone} today!"[:155]

    # Generate page slug
    slug = keyword.lower().replace(" ", "-") + f"-{location.lower()}"

    return {
        "title": h1,
        "slug": slug,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "h1": h1,
        "keyword": keyword,
        "location": location,
        "business_name": business_name,
        "phone": phone,
    }


def create_elementor_structure(content: dict, site_config: dict) -> dict:
    """Create Elementor-compatible page structure."""

    # Load template sections
    sections = []
    template_files = [
        "hero-section.json",
        "trust-signals.json",
        "service-features.json",
        "cta-section.json",
        "contact-form.json"
    ]

    for template_file in template_files:
        template_path = TEMPLATES_DIR / "elementor" / template_file
        if template_path.exists():
            with open(template_path) as f:
                section = json.load(f)
                # Replace placeholders with actual content
                section_str = json.dumps(section)
                section_str = section_str.replace("{{H1}}", content["h1"])
                section_str = section_str.replace("{{PHONE}}", content["phone"])
                section_str = section_str.replace("{{BUSINESS_NAME}}", content["business_name"])
                section_str = section_str.replace("{{LOCATION}}", content["location"])
                section_str = section_str.replace("{{KEYWORD}}", content["keyword"])
                sections.append(json.loads(section_str))

    return {
        "version": "0.4",
        "title": content["title"],
        "type": "page",
        "content": sections
    }


def deploy_page(site_config: dict, content: dict, elementor_data: dict) -> dict:
    """Deploy page to WordPress via SSH/WP-CLI."""

    wp = WordPressClient(
        host=site_config["ssh_host"],
        port=site_config.get("ssh_port", 22),
        user=site_config["ssh_user"],
        key_path=site_config.get("ssh_key", "~/.ssh/id_ed25519"),
        wp_path=site_config["wp_path"]
    )

    # Create the page
    result = wp.create_page(
        title=content["title"],
        slug=content["slug"],
        status="draft"  # Start as draft for review
    )

    page_id = result.get("page_id")
    if not page_id:
        raise RuntimeError("Failed to create page")

    # Set meta tags
    wp.update_meta(page_id, "_yoast_wpseo_title", content["meta_title"])
    wp.update_meta(page_id, "_yoast_wpseo_metadesc", content["meta_description"])

    # Import Elementor data (if supported)
    # Note: This requires Elementor to be active
    try:
        wp.import_elementor_template(page_id, elementor_data)
    except Exception as e:
        print(f"Warning: Could not import Elementor template: {e}")

    # Generate and inject schema
    schema = generate_local_business_schema(site_config)
    wp.inject_schema(page_id, schema)

    # Get page URL
    page_url = wp.get_page_url(page_id)

    return {
        "page_id": page_id,
        "page_url": page_url,
        "status": "draft",
        "title": content["title"],
        "slug": content["slug"]
    }


def run_performance_audit(url: str) -> dict:
    """Run PageSpeed Insights audit on deployed page."""
    try:
        # Use PageSpeed Insights API
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
        result = subprocess.run(
            ["curl", "-s", api_url],
            capture_output=True,
            text=True,
            timeout=60
        )
        data = json.loads(result.stdout)

        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})

        return {
            "performance": categories.get("performance", {}).get("score", 0) * 100,
            "accessibility": categories.get("accessibility", {}).get("score", 0) * 100,
            "best_practices": categories.get("best-practices", {}).get("score", 0) * 100,
            "seo": categories.get("seo", {}).get("score", 0) * 100,
            "lcp": lighthouse.get("audits", {}).get("largest-contentful-paint", {}).get("displayValue", "N/A"),
            "cls": lighthouse.get("audits", {}).get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
            "fid": lighthouse.get("audits", {}).get("max-potential-fid", {}).get("displayValue", "N/A"),
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Deploy optimized landing page")
    parser.add_argument("--site", required=True, help="Site config name (e.g., jlr_smith_roofing)")
    parser.add_argument("--keyword", required=True, help="Target keyword for the page")
    parser.add_argument("--publish", action="store_true", help="Publish immediately (default: draft)")
    parser.add_argument("--audit", action="store_true", help="Run performance audit after deployment")

    args = parser.parse_args()

    print(f"=" * 60)
    print(f"Landing Page Deployment")
    print(f"Site: {args.site}")
    print(f"Keyword: {args.keyword}")
    print(f"=" * 60)

    # Load site configuration
    print("\n[1/5] Loading site configuration...")
    site_config = load_site_config(args.site)
    print(f"  Business: {site_config.get('business_name')}")
    print(f"  Location: {site_config.get('location')}")

    # Generate page content
    print("\n[2/5] Generating page content...")
    content = generate_page_content(args.keyword, site_config)
    print(f"  Title: {content['title']}")
    print(f"  Slug: {content['slug']}")
    print(f"  Meta: {content['meta_title']}")

    # Create Elementor structure
    print("\n[3/5] Building Elementor structure...")
    elementor_data = create_elementor_structure(content, site_config)
    print(f"  Sections: {len(elementor_data.get('content', []))}")

    # Deploy to WordPress
    print("\n[4/5] Deploying to WordPress...")
    try:
        result = deploy_page(site_config, content, elementor_data)
        print(f"  Page ID: {result['page_id']}")
        print(f"  URL: {result['page_url']}")
        print(f"  Status: {result['status']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        print("\n  SSH deployment failed. Ensure:")
        print("    - SSH key is configured and authorized")
        print("    - WP-CLI is installed on server")
        print("    - Site config has correct paths")
        return 1

    # Run performance audit
    if args.audit and result.get("page_url"):
        print("\n[5/5] Running performance audit...")
        audit = run_performance_audit(result["page_url"])
        if "error" not in audit:
            print(f"  Performance: {audit.get('performance', 'N/A')}")
            print(f"  Accessibility: {audit.get('accessibility', 'N/A')}")
            print(f"  Best Practices: {audit.get('best_practices', 'N/A')}")
            print(f"  SEO: {audit.get('seo', 'N/A')}")
            print(f"  LCP: {audit.get('lcp', 'N/A')}")
            print(f"  CLS: {audit.get('cls', 'N/A')}")
        else:
            print(f"  Audit error: {audit['error']}")

    print("\n" + "=" * 60)
    print("Deployment complete!")
    print("=" * 60)

    # Log deployment
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "site": args.site,
        "keyword": args.keyword,
        "result": result
    }
    log_path = SCRIPT_DIR.parent / "deployment_log.json"

    try:
        if log_path.exists():
            with open(log_path) as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(log_path, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not write log: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
