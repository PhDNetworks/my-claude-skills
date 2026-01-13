#!/usr/bin/env python3
"""
Performance Optimizer for Landing Pages

Handles image optimization, critical CSS extraction, and
Core Web Vitals improvements.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import base64
import hashlib


class PerformanceOptimizer:
    """Optimize landing page performance for Core Web Vitals."""

    # Target thresholds (Google's "Good" thresholds)
    TARGETS = {
        "lcp": 2.5,       # Largest Contentful Paint (seconds)
        "cls": 0.1,       # Cumulative Layout Shift (score)
        "inp": 200,       # Interaction to Next Paint (milliseconds)
        "ttfb": 0.8,      # Time to First Byte (seconds)
        "fcp": 1.8,       # First Contentful Paint (seconds)
    }

    def __init__(self, wp_client=None):
        """
        Initialize optimizer.

        Args:
            wp_client: Optional WordPressClient for remote operations
        """
        self.wp_client = wp_client

    # ========== Image Optimization ==========

    def optimize_image(
        self,
        image_path: str,
        max_width: int = 1200,
        quality: int = 85,
        format: str = "webp"
    ) -> Dict:
        """
        Optimize image for web.

        Requires: ImageMagick (convert) or libvips (vips)
        """
        input_path = Path(image_path)
        output_path = input_path.with_suffix(f".{format}")

        # Get original size
        original_size = input_path.stat().st_size

        # Try using ImageMagick
        try:
            cmd = [
                "convert",
                str(input_path),
                "-resize", f"{max_width}x>",  # Only shrink if larger
                "-quality", str(quality),
                "-strip",  # Remove metadata
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)

            new_size = output_path.stat().st_size
            savings = ((original_size - new_size) / original_size) * 100

            return {
                "success": True,
                "original_path": str(input_path),
                "optimized_path": str(output_path),
                "original_size": original_size,
                "new_size": new_size,
                "savings_percent": round(savings, 1),
                "format": format
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "original_path": str(input_path)
            }

    def generate_responsive_images(
        self,
        image_path: str,
        widths: List[int] = [320, 640, 960, 1280, 1920]
    ) -> Dict:
        """Generate multiple sizes for srcset."""

        input_path = Path(image_path)
        results = []

        for width in widths:
            output_path = input_path.stem + f"-{width}w" + input_path.suffix
            result = self.optimize_image(
                str(input_path),
                max_width=width,
                format="webp"
            )
            results.append({
                "width": width,
                "path": result.get("optimized_path"),
                "size": result.get("new_size")
            })

        # Generate srcset string
        srcset = ", ".join([
            f"{r['path']} {r['width']}w"
            for r in results if r.get('path')
        ])

        return {
            "images": results,
            "srcset": srcset,
            "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        }

    # ========== Critical CSS ==========

    def extract_critical_css(self, html_content: str, css_content: str) -> str:
        """
        Extract critical (above-fold) CSS.

        For production, consider using:
        - critical (npm package)
        - penthouse (npm package)
        """
        # Basic implementation - extracts CSS for common critical selectors
        critical_selectors = [
            # Reset/base
            "*", "html", "body",
            # Header/navigation
            "header", "nav", ".header", ".nav", ".navbar",
            # Hero section
            ".hero", ".hero-section", "#hero",
            ".elementor-section-wrap > .elementor-section:first-child",
            # Typography
            "h1", "h2", ".title", ".heading",
            # CTA
            ".btn", ".button", ".cta",
            # Layout
            ".container", ".wrapper", ".row",
            # Trust signals (above fold)
            ".trust", ".rating", ".reviews"
        ]

        # This is a simplified version - production should use a proper
        # critical CSS extraction tool
        return """
/* Critical CSS - Above Fold */
*,*::before,*::after{box-sizing:border-box}
html{font-size:16px;-webkit-text-size-adjust:100%}
body{margin:0;font-family:system-ui,-apple-system,sans-serif;line-height:1.5}
h1,h2,h3{margin-top:0;font-weight:700}
img{max-width:100%;height:auto;display:block}
.hero-section{min-height:60vh;display:flex;align-items:center}
.container{width:100%;max-width:1200px;margin:0 auto;padding:0 1rem}
.btn,.button{display:inline-block;padding:.75rem 1.5rem;font-weight:600;text-decoration:none;border-radius:.25rem;cursor:pointer}
"""

    def inline_critical_css(self, html: str, critical_css: str) -> str:
        """Inline critical CSS into HTML head."""

        style_tag = f"<style>{critical_css}</style>"

        # Insert before </head>
        if "</head>" in html:
            return html.replace("</head>", f"{style_tag}\n</head>")
        return style_tag + html

    # ========== Resource Hints ==========

    def generate_preload_hints(self, resources: List[Dict]) -> str:
        """
        Generate preload/preconnect link tags.

        Args:
            resources: List of {"url": "...", "type": "font|image|script|style"}
        """
        hints = []

        # Common preconnects
        preconnects = [
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com",
            "https://www.googletagmanager.com",
        ]

        for url in preconnects:
            hints.append(f'<link rel="preconnect" href="{url}" crossorigin>')

        # Resource-specific preloads
        for resource in resources:
            url = resource.get("url", "")
            res_type = resource.get("type", "")

            if res_type == "font":
                hints.append(
                    f'<link rel="preload" href="{url}" as="font" type="font/woff2" crossorigin>'
                )
            elif res_type == "image":
                hints.append(f'<link rel="preload" href="{url}" as="image">')
            elif res_type == "script":
                hints.append(f'<link rel="preload" href="{url}" as="script">')
            elif res_type == "style":
                hints.append(f'<link rel="preload" href="{url}" as="style">')

        return "\n".join(hints)

    # ========== Lazy Loading ==========

    def add_lazy_loading(self, html: str) -> str:
        """Add native lazy loading to images below fold."""

        # Add loading="lazy" to img tags (except hero/LCP images)
        # This is simplified - production should identify LCP image

        import re

        def add_lazy(match):
            img_tag = match.group(0)
            # Skip if already has loading attribute or is hero image
            if 'loading=' in img_tag or 'hero' in img_tag.lower():
                return img_tag
            # Add loading="lazy" before closing >
            return img_tag.replace('>', ' loading="lazy">', 1)

        return re.sub(r'<img[^>]+>', add_lazy, html)

    # ========== Font Optimization ==========

    def optimize_fonts(self, font_families: List[str]) -> Dict:
        """Generate optimized font loading strategy."""

        # Use font-display: swap
        font_face_css = ""
        preloads = []

        for family in font_families:
            # Google Fonts URL with display=swap
            url = f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}&display=swap"
            preloads.append(url)

        return {
            "preload_links": [
                f'<link rel="preconnect" href="https://fonts.googleapis.com">',
                f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            ],
            "stylesheet_links": [
                f'<link rel="stylesheet" href="{url}">'
                for url in preloads
            ],
            "font_display": "swap"
        }

    # ========== JavaScript Optimization ==========

    def defer_non_critical_js(self, html: str) -> str:
        """Add defer/async to non-critical scripts."""

        import re

        def add_defer(match):
            script_tag = match.group(0)
            # Skip if already has defer/async or is inline
            if 'defer' in script_tag or 'async' in script_tag:
                return script_tag
            if 'src=' not in script_tag:
                return script_tag
            # Critical scripts to NOT defer
            critical = ['gtag', 'analytics', 'jquery']
            if any(c in script_tag.lower() for c in critical):
                return script_tag
            return script_tag.replace('<script', '<script defer')

        return re.sub(r'<script[^>]*>', add_defer, html)

    # ========== Audit ==========

    def run_audit(self, url: str) -> Dict:
        """
        Run PageSpeed Insights audit.

        Returns Core Web Vitals and recommendations.
        """
        try:
            api_url = (
                f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                f"?url={url}&strategy=mobile"
                f"&category=performance&category=accessibility"
                f"&category=best-practices&category=seo"
            )

            result = subprocess.run(
                ["curl", "-s", api_url],
                capture_output=True,
                text=True,
                timeout=120
            )

            data = json.loads(result.stdout)
            lighthouse = data.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})
            categories = lighthouse.get("categories", {})

            return {
                "url": url,
                "scores": {
                    "performance": int((categories.get("performance", {}).get("score", 0) or 0) * 100),
                    "accessibility": int((categories.get("accessibility", {}).get("score", 0) or 0) * 100),
                    "best_practices": int((categories.get("best-practices", {}).get("score", 0) or 0) * 100),
                    "seo": int((categories.get("seo", {}).get("score", 0) or 0) * 100),
                },
                "core_web_vitals": {
                    "lcp": audits.get("largest-contentful-paint", {}).get("numericValue", 0) / 1000,
                    "cls": audits.get("cumulative-layout-shift", {}).get("numericValue", 0),
                    "fid": audits.get("max-potential-fid", {}).get("numericValue", 0),
                    "fcp": audits.get("first-contentful-paint", {}).get("numericValue", 0) / 1000,
                    "ttfb": audits.get("server-response-time", {}).get("numericValue", 0) / 1000,
                },
                "opportunities": [
                    {
                        "id": key,
                        "title": audit.get("title", ""),
                        "savings": audit.get("numericValue", 0)
                    }
                    for key, audit in audits.items()
                    if audit.get("score", 1) < 0.9 and audit.get("numericValue", 0) > 0
                ][:10]  # Top 10 opportunities
            }

        except Exception as e:
            return {"error": str(e), "url": url}

    def check_cwv_pass(self, audit_result: Dict) -> Dict:
        """Check if Core Web Vitals pass thresholds."""

        cwv = audit_result.get("core_web_vitals", {})

        return {
            "lcp": {
                "value": cwv.get("lcp", 0),
                "target": self.TARGETS["lcp"],
                "pass": cwv.get("lcp", 999) <= self.TARGETS["lcp"]
            },
            "cls": {
                "value": cwv.get("cls", 0),
                "target": self.TARGETS["cls"],
                "pass": cwv.get("cls", 999) <= self.TARGETS["cls"]
            },
            "fid": {
                "value": cwv.get("fid", 0),
                "target": self.TARGETS["inp"],
                "pass": cwv.get("fid", 999) <= self.TARGETS["inp"]
            },
            "overall_pass": all([
                cwv.get("lcp", 999) <= self.TARGETS["lcp"],
                cwv.get("cls", 999) <= self.TARGETS["cls"],
                cwv.get("fid", 999) <= self.TARGETS["inp"]
            ])
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python performance_optimizer.py <url>")
        sys.exit(1)

    optimizer = PerformanceOptimizer()
    url = sys.argv[1]

    print(f"Auditing: {url}")
    result = optimizer.run_audit(url)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"\nScores:")
    for key, value in result["scores"].items():
        print(f"  {key}: {value}")

    print(f"\nCore Web Vitals:")
    cwv_check = optimizer.check_cwv_pass(result)
    for metric, data in cwv_check.items():
        if metric != "overall_pass":
            status = "✓" if data["pass"] else "✗"
            print(f"  {metric}: {data['value']:.2f} (target: {data['target']}) {status}")

    print(f"\n  Overall: {'PASS' if cwv_check['overall_pass'] else 'FAIL'}")

    if result.get("opportunities"):
        print(f"\nTop Opportunities:")
        for opp in result["opportunities"][:5]:
            print(f"  - {opp['title']}")
