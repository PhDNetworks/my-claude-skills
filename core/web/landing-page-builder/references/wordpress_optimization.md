# WordPress Landing Page Optimization Guide

## Overview

This guide covers WordPress-specific optimizations for landing pages targeting:
- Lighthouse Performance Score > 90
- Core Web Vitals in "Good" range
- Google Ads Quality Score "Above Average"

---

## Server Requirements

### Minimum Specifications

```markdown
PHP Version: 8.1+ (8.2 recommended)
MySQL Version: 8.0+ or MariaDB 10.4+
Web Server: Apache 2.4+ or Nginx 1.18+
Memory: 256MB PHP memory limit minimum
Storage: SSD required for production
```

### Recommended Hosting Features

```markdown
□ LiteSpeed or Nginx (faster than Apache)
□ PHP OPcache enabled
□ Redis or Memcached for object caching
□ HTTP/2 or HTTP/3 support
□ SSL/TLS certificate
□ CDN integration
□ Automatic backups
```

---

## WordPress Configuration

### wp-config.php Optimizations

```php
<?php
// Memory settings
define('WP_MEMORY_LIMIT', '256M');
define('WP_MAX_MEMORY_LIMIT', '512M');

// Performance settings
define('WP_POST_REVISIONS', 3);
define('AUTOSAVE_INTERVAL', 300);
define('EMPTY_TRASH_DAYS', 7);

// Security (also improves performance)
define('DISALLOW_FILE_EDIT', true);
define('WP_AUTO_UPDATE_CORE', true);

// Debug (disable in production)
define('WP_DEBUG', false);
define('WP_DEBUG_LOG', false);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', false);

// Caching
define('WP_CACHE', true);
```

### .htaccess Performance Rules

```apache
# Enable GZIP compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml
    AddOutputFilterByType DEFLATE text/css text/javascript
    AddOutputFilterByType DEFLATE application/javascript application/x-javascript
    AddOutputFilterByType DEFLATE application/json application/xml
    AddOutputFilterByType DEFLATE application/rss+xml application/atom+xml
    AddOutputFilterByType DEFLATE image/svg+xml
</IfModule>

# Browser caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresDefault "access plus 1 month"

    # Images
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/x-icon "access plus 1 year"

    # CSS/JS
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"

    # Fonts
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType application/font-woff2 "access plus 1 year"

    # HTML
    ExpiresByType text/html "access plus 0 seconds"
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Disable ETags
<IfModule mod_headers.c>
    Header unset ETag
</IfModule>
FileETag None
```

---

## Plugin Stack

### Essential Plugins Only

For landing pages, minimize plugins to reduce overhead:

```markdown
REQUIRED:
□ Elementor Pro - Page builder
□ WP Rocket OR LiteSpeed Cache - Caching & optimization

OPTIONAL (based on need):
□ Rank Math / Yoast SEO - SEO meta (choose one)
□ WPForms Lite / Elementor Forms - Contact forms
□ ShortPixel / Imagify - Image optimization

AVOID:
✗ Multiple caching plugins
✗ Social sharing plugins
✗ Slider plugins (use Elementor carousel if needed)
✗ Page builder addons (Elementor addons packs)
✗ Analytics plugins (use gtag.js directly)
```

### Plugin Configuration: WP Rocket

```markdown
Cache:
□ Mobile Cache: ON
□ User Cache: OFF (for landing pages)
□ Cache Lifespan: 10 hours

File Optimization:
□ Minify CSS: ON
□ Combine CSS: OFF (HTTP/2)
□ Optimize CSS Delivery: ON (Remove Unused CSS)
□ Minify JavaScript: ON
□ Combine JavaScript: OFF (HTTP/2)
□ Load JavaScript Deferred: ON

Media:
□ LazyLoad images: ON
□ LazyLoad iframes: ON
□ Add missing dimensions: ON
□ WebP compatibility: ON

Preload:
□ Preload Cache: ON
□ Preload Links: ON
□ Prefetch DNS: Add CDN and analytics domains

Advanced:
□ Exclude jQuery from defer (if issues)

CDN:
□ Enable CDN: ON (if using)
□ CDN CNAME: cdn.yourdomain.com

Heartbeat:
□ Reduce activity: Everywhere
□ Frequency: 60 seconds
```

### Plugin Configuration: LiteSpeed Cache

```markdown
General:
□ Enable LiteSpeed Cache: ON

Cache:
□ Cache Logged-in Users: OFF
□ Cache Mobile: ON (separate cache)
□ Private Cached URIs: /cart /checkout

TTL:
□ Default Public: 604800 (1 week)
□ Default Front Page: 604800

Purge:
□ Purge All On Upgrade: ON
□ Auto Purge: All pages when post updated

Page Optimization:
□ CSS Minify: ON
□ CSS Combine: OFF
□ Generate UCSS: ON
□ UCSS Inline: ON
□ CSS HTTP/2 Push: OFF
□ Load CSS Asynchronously: ON
□ JS Minify: ON
□ JS Combine: OFF
□ JS HTTP/2 Push: OFF
□ Load JS Deferred: ON

Media:
□ Lazy Load Images: ON
□ Add Missing Sizes: ON
□ WebP Replacement: ON
□ Preload Featured Image: ON

CDN:
□ Enable CDN: ON (QUIC.cloud or other)
```

---

## Elementor Optimization

### Global Settings

Navigate to: Elementor > Settings

```markdown
General:
□ Disable Default Colors: ON
□ Disable Default Fonts: ON

Integrations:
□ Google Fonts: Load from your server (or disable)
□ Font Awesome: Only load when used

Advanced:
□ CSS Print Method: External File
□ Google Fonts Load: Swap
□ Load Font Awesome 4: OFF

Performance (Elementor 3.0+):
□ Improved Asset Loading: ON
□ Improved CSS Loading: ON
□ Flexbox Container: ON (use containers, not sections)
```

### Page-Level Settings

For each landing page:

```markdown
Page Settings > Layout:
□ Page Layout: Elementor Full Width
□ Hide Title: ON

Page Settings > Style:
□ Body Background: Set here (not in section)

Custom CSS (if needed):
□ Add to page settings, not global
```

### Elementor Best Practices

```markdown
DO:
✓ Use Flexbox Containers (not legacy sections)
✓ Set explicit image sizes
✓ Use system fonts or limit to 2 font families
✓ Use native lazy loading
✓ Minimize widget count (< 50 per page)

DON'T:
✗ Use background videos (high LCP impact)
✗ Add excessive animations
✗ Use multiple slider widgets
✗ Import demo content
✗ Install Elementor addon packs
```

---

## Image Optimization

### Before Upload

```markdown
Format Selection:
- Photos: WebP (JPEG fallback)
- Graphics/logos: SVG or WebP (PNG fallback)
- Icons: SVG (inline when possible)

Size Guidelines:
- Hero images: 1920x1080 max (often 1200x600 sufficient)
- Service cards: 400x300
- Thumbnails: 150x150
- Always export at 1x and 2x for retina
```

### ShortPixel Settings

```markdown
General:
□ Compression Type: Lossy (best balance)
□ Include Thumbnails: ON
□ Create WebP: ON
□ Resize Large Images: ON (max 1920px width)
□ Remove EXIF: ON

Advanced:
□ Process in Front-End: OFF
□ CloudFlare Integration: ON (if using)
```

### Manual Image Optimization

```bash
# Using squoosh-cli
npx @aspect/cli image compress hero.jpg --quality 80 --format webp

# Using cwebp
cwebp -q 80 input.jpg -o output.webp

# Using imagemagick
convert input.jpg -resize 1200x -quality 85 -strip output.jpg
```

---

## Database Optimization

### Cleanup Tasks (Monthly)

```sql
-- Delete post revisions (keep 3)
DELETE FROM wp_posts WHERE post_type = 'revision';

-- Delete orphaned post meta
DELETE pm FROM wp_postmeta pm
LEFT JOIN wp_posts wp ON wp.ID = pm.post_id
WHERE wp.ID IS NULL;

-- Delete expired transients
DELETE FROM wp_options WHERE option_name LIKE '_transient_%'
AND option_name NOT LIKE '_transient_timeout_%';

-- Optimize tables
OPTIMIZE TABLE wp_posts, wp_postmeta, wp_options;
```

### WP-CLI Database Commands

```bash
# Delete revisions
wp post delete $(wp post list --post_type='revision' --format=ids)

# Delete transients
wp transient delete --expired

# Optimize database
wp db optimize

# Search-replace (for migrations)
wp search-replace 'old-domain.com' 'new-domain.com' --dry-run
```

---

## WP-CLI Commands for Landing Pages

### Page Creation

```bash
# Create landing page
wp post create --post_type=page \
  --post_title="Roofing Services Leeds" \
  --post_status=publish \
  --post_name="roofing-leeds"

# Set page template
wp post meta update $POST_ID _wp_page_template "elementor_header_footer"

# Set Elementor data
wp post meta update $POST_ID _elementor_edit_mode "builder"
wp post meta update $POST_ID _elementor_template_type "wp-page"
```

### Cache Management

```bash
# WP Rocket
wp rocket clean --confirm

# LiteSpeed Cache
wp litespeed-purge all

# General
wp cache flush
```

### Performance Audit

```bash
# Check site health
wp site health status

# List active plugins
wp plugin list --status=active

# Check database size
wp db size --tables

# Get Core Web Vitals from API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile"
```

---

## Pre-Launch Checklist

### Technical Checks

```markdown
□ SSL certificate installed and forced
□ HTTP to HTTPS redirect working
□ www/non-www redirect set
□ Cache plugin configured
□ Image optimization complete
□ Unused plugins deactivated
□ Debug mode disabled
□ Search engines allowed (if not staging)
```

### Performance Checks

```markdown
□ PageSpeed Insights > 90 mobile
□ LCP < 2.5s
□ CLS < 0.1
□ INP < 200ms
□ No render-blocking resources
□ Images have width/height
□ Fonts preloaded
□ Critical CSS inlined
```

### SEO Checks

```markdown
□ Title tag set (< 60 chars)
□ Meta description set (< 160 chars)
□ H1 contains keyword
□ Schema markup added
□ Open Graph tags set
□ Canonical URL correct
□ Robots meta appropriate
□ XML sitemap updated
```

### Tracking Checks

```markdown
□ GA4 installed and firing
□ Google Ads conversion tracking
□ Phone tracking configured
□ Form submission tracking
□ Goals/conversions set up
□ Tag Manager (if used) deployed
```

---

## Troubleshooting

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| LCP > 4s | Unoptimized hero image | Compress, use WebP, preload |
| CLS > 0.25 | Images without dimensions | Add width/height attributes |
| White screen | PHP memory limit | Increase WP_MEMORY_LIMIT |
| 500 errors | Plugin conflict | Disable plugins via FTP |
| Cache not working | Config issue | Check wp-config.php WP_CACHE |
| Fonts flash | FOUT | Preload fonts, font-display: swap |

### Debug Mode (Temporary)

```php
// Add to wp-config.php temporarily
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);

// Check log at: /wp-content/debug.log
```

### Emergency Recovery

```bash
# Disable all plugins via WP-CLI
wp plugin deactivate --all

# Switch to default theme
wp theme activate twentytwentyfour

# Reset permalinks
wp rewrite flush

# Check for fatal errors
wp eval "echo 'WordPress loaded';"
```
