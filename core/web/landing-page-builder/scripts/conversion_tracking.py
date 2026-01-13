#!/usr/bin/env python3
"""
Conversion Tracking Setup

Configure GA4 and Google Ads conversion tracking for landing pages.
"""

import json
from typing import Dict, List, Optional


def generate_gtag_snippet(
    ga4_id: str,
    ads_id: Optional[str] = None,
    conversion_actions: Optional[List[Dict]] = None
) -> str:
    """
    Generate Google Tag (gtag.js) snippet.

    Args:
        ga4_id: GA4 Measurement ID (G-XXXXXXXX)
        ads_id: Google Ads ID (AW-XXXXXXXXX) - optional
        conversion_actions: List of conversion action configs

    Returns:
        HTML snippet to include in <head>
    """

    # Base gtag snippet
    snippet = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{ga4_id}');'''

    # Add Google Ads config if provided
    if ads_id:
        snippet += f"\n  gtag('config', '{ads_id}');"

    snippet += "\n</script>"

    return snippet


def generate_phone_tracking_snippet(
    phone_number: str,
    ads_conversion_id: Optional[str] = None,
    ads_conversion_label: Optional[str] = None
) -> str:
    """
    Generate phone click tracking snippet.

    Tracks:
    - GA4 event: phone_click
    - Google Ads phone call conversion (if configured)
    """

    snippet = f'''<script>
// Phone click tracking
document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {{
  link.addEventListener('click', function(e) {{
    // GA4 event
    gtag('event', 'phone_click', {{
      'event_category': 'contact',
      'event_label': this.href.replace('tel:', ''),
      'phone_number': '{phone_number}'
    }});'''

    if ads_conversion_id and ads_conversion_label:
        snippet += f'''

    // Google Ads conversion
    gtag('event', 'conversion', {{
      'send_to': '{ads_conversion_id}/{ads_conversion_label}',
      'value': 1.0,
      'currency': 'GBP'
    }});'''

    snippet += '''
  });
});
</script>'''

    return snippet


def generate_form_tracking_snippet(
    form_selector: str = "form",
    conversion_name: str = "form_submission"
) -> str:
    """
    Generate form submission tracking snippet.

    Tracks form submissions as conversions.
    """

    return f'''<script>
// Form submission tracking
document.querySelectorAll('{form_selector}').forEach(function(form) {{
  form.addEventListener('submit', function(e) {{
    // GA4 event
    gtag('event', '{conversion_name}', {{
      'event_category': 'form',
      'event_label': this.id || 'contact_form'
    }});

    // Allow form to submit
    return true;
  }});
}});
</script>'''


def generate_scroll_tracking_snippet(thresholds: List[int] = [25, 50, 75, 90]) -> str:
    """
    Generate scroll depth tracking snippet.

    Tracks how far users scroll down the page.
    """

    return f'''<script>
// Scroll depth tracking
(function() {{
  var scrollThresholds = {json.dumps(thresholds)};
  var trackedThresholds = {{}};

  function getScrollPercent() {{
    var h = document.documentElement,
        b = document.body,
        st = 'scrollTop',
        sh = 'scrollHeight';
    return Math.round((h[st] || b[st]) / ((h[sh] || b[sh]) - h.clientHeight) * 100);
  }}

  window.addEventListener('scroll', function() {{
    var percent = getScrollPercent();

    scrollThresholds.forEach(function(threshold) {{
      if (percent >= threshold && !trackedThresholds[threshold]) {{
        trackedThresholds[threshold] = true;

        gtag('event', 'scroll_depth', {{
          'event_category': 'engagement',
          'event_label': threshold + '%',
          'value': threshold
        }});
      }}
    }});
  }});
}})();
</script>'''


def generate_cta_tracking_snippet() -> str:
    """
    Generate CTA button click tracking.

    Tracks clicks on buttons with class 'cta', 'btn-primary', etc.
    """

    return '''<script>
// CTA click tracking
document.querySelectorAll('.cta, .btn-primary, [data-track="cta"]').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    gtag('event', 'cta_click', {
      'event_category': 'engagement',
      'event_label': this.textContent.trim().substring(0, 50),
      'cta_location': this.closest('section')?.id || 'unknown'
    });
  });
});
</script>'''


def generate_engagement_tracking_snippet(
    time_thresholds: List[int] = [30, 60, 120, 300]
) -> str:
    """
    Generate time on page engagement tracking.

    Args:
        time_thresholds: Seconds at which to fire events
    """

    return f'''<script>
// Time on page tracking
(function() {{
  var timeThresholds = {json.dumps(time_thresholds)};
  var trackedTimes = {{}};
  var startTime = Date.now();

  setInterval(function() {{
    var elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);

    timeThresholds.forEach(function(threshold) {{
      if (elapsedSeconds >= threshold && !trackedTimes[threshold]) {{
        trackedTimes[threshold] = true;

        gtag('event', 'time_on_page', {{
          'event_category': 'engagement',
          'event_label': threshold + ' seconds',
          'value': threshold
        }});
      }}
    }});
  }}, 5000); // Check every 5 seconds
}})();
</script>'''


def setup_ga4_tracking(site_config: Dict) -> str:
    """
    Generate complete tracking setup for a landing page.

    Args:
        site_config: Site configuration with tracking IDs

    Returns:
        Complete tracking code to inject
    """

    ga4_id = site_config.get("ga4_id")
    ads_id = site_config.get("google_ads_id")
    phone = site_config.get("phone", "")

    if not ga4_id:
        return "<!-- GA4 ID not configured -->"

    snippets = []

    # 1. Base gtag snippet
    snippets.append(generate_gtag_snippet(ga4_id, ads_id))

    # 2. Phone tracking
    if phone:
        snippets.append(generate_phone_tracking_snippet(
            phone,
            ads_id,
            site_config.get("ads_phone_conversion_label")
        ))

    # 3. Form tracking
    snippets.append(generate_form_tracking_snippet())

    # 4. Scroll tracking
    snippets.append(generate_scroll_tracking_snippet())

    # 5. CTA tracking
    snippets.append(generate_cta_tracking_snippet())

    # 6. Engagement tracking
    snippets.append(generate_engagement_tracking_snippet())

    return "\n\n".join(snippets)


def generate_gtm_container_snippet(gtm_id: str) -> str:
    """
    Generate Google Tag Manager container snippet.

    Returns both head and body snippets.
    """

    head_snippet = f'''<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');</script>
<!-- End Google Tag Manager -->'''

    body_snippet = f'''<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'''

    return {
        "head": head_snippet,
        "body": body_snippet
    }


if __name__ == "__main__":
    # Example configuration
    config = {
        "ga4_id": "G-XXXXXXXXXX",
        "google_ads_id": "AW-XXXXXXXXXX",
        "phone": "0113 XXX XXXX",
        "ads_phone_conversion_label": "XXXXXXXXXX"
    }

    print("Generated tracking code:")
    print("=" * 60)
    print(setup_ga4_tracking(config))
