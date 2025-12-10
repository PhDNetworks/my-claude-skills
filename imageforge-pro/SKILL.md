---
name: imageforge-pro
description: Professional image optimization for web projects. Batch rename images with SEO-friendly filenames, generate alt text, embed metadata, and optionally upload directly to WordPress. Use when user wants to rename images for SEO, prepare images for a website, optimize image filenames, generate alt text, process a folder of images with descriptive names, or upload images to WordPress with alt text. Supports trades/services (roofing, electrical, plumbing, building, windows, landscaping, cleaning, dental, etc.), products, and general imagery. Triggers include "rename images", "SEO images", "image optimization", "alt text", "prepare images for website", "upload to WordPress".
---

# ImageForge Pro

Professional image optimization workflow for web projects. Transforms generic camera filenames into SEO-optimized, descriptive filenames with alt text generation and automated deployment options.

## Interactive Workflow

When triggered, follow this decision flow:

### Step 1: Gather Requirements

Ask the user:
1. **Folder path** - Where are the images located?
2. **Industry/context** - What type of business? (See `references/industry-keywords.md`)
3. **Location** - Geographic area for local SEO? (e.g., Leeds, West Yorkshire)

### Step 2: Determine Output Pathway

Ask: "How would you like to use these images?"

**Pathway A - Rename Only**
- Rename files locally
- Generate manifest CSV with alt text suggestions
- User uploads manually to their CMS

**Pathway B - EXIF Embedding**
- Rename files
- Embed alt text into JPEG EXIF metadata (ImageDescription field)
- Alt text auto-populates when uploaded to most CMS platforms

**Pathway C - WordPress Direct Upload**
- Rename files
- Upload via WordPress REST API
- Alt text, title, and caption set automatically
- *Requires:* Site URL, username, application password

### Step 3: Execute

Run the unified script based on chosen pathway:

```bash
# Pathway A: Rename only
python3 scripts/imageforge.py /path/to/folder --mode rename --industry roofing --location leeds

# Pathway B: Rename + EXIF embed
python3 scripts/imageforge.py /path/to/folder --mode embed --industry roofing --location leeds

# Pathway C: WordPress upload
python3 scripts/imageforge.py /path/to/folder --mode wordpress \
  --industry roofing --location leeds \
  --wp-site https://example.com \
  --wp-user admin \
  --wp-password "xxxx xxxx xxxx xxxx"
```

## Script Usage

### Core Commands

```bash
# List images in folder
python3 scripts/imageforge.py /path/to/folder --list

# Preview renames (dry run)
python3 scripts/imageforge.py /path/to/folder --mode rename --dry-run

# Generate CSV template for manual editing
python3 scripts/imageforge.py /path/to/folder --template
```

### Full Options

| Flag | Description |
|------|-------------|
| `--mode` | `rename`, `embed`, or `wordpress` |
| `--industry` | Business type for keyword context |
| `--location` | Geographic suffix for local SEO |
| `--dry-run` | Preview without making changes |
| `--list` | Show images in folder |
| `--template` | Generate CSV template for batch editing |
| `--from-csv` | Apply renames from edited CSV file |
| `--wp-site` | WordPress site URL (for wordpress mode) |
| `--wp-user` | WordPress username |
| `--wp-password` | WordPress application password |
| `--backup` | Keep original files with .bak extension |

## Naming Conventions

- Lowercase only
- Hyphens between words (no underscores or spaces)
- 3-6 descriptive words maximum
- Pattern: `[action]-[material/type]-[context]-[location].[ext]`

**Examples:**
| Before | After |
|--------|-------|
| IMG_4532.jpg | slate-roof-repair-terraced-house-leeds.jpg |
| DSC0001.png | ev-charger-installation-driveway-leeds.png |
| photo_2024.jpg | dental-surgery-modern-interior-leeds.jpg |
| 20240115_093422.jpg | upvc-fascia-replacement-semi-detached.jpg |

## Output Files

| File | Description |
|------|-------------|
| `imageforge_manifest.csv` | Mapping of old → new filenames with alt text |
| `imageforge_log.txt` | Processing log with timestamps |

## Alt Text Generation

Alt text follows this pattern:
- **Format:** "[Descriptive phrase] in [location]"
- **Length:** 80-125 characters
- **Include:** Action, materials, context, location
- **Exclude:** "Image of", "Photo of", file extensions

**Example alt text:**
> Professional slate roof repair on Victorian terraced house in Leeds, West Yorkshire

## WordPress Application Passwords

For WordPress upload pathway, guide user to create application password:

1. Log into WordPress admin
2. Go to **Users → Your Profile**
3. Scroll to **Application Passwords**
4. Enter name (e.g., "ImageForge Pro")
5. Click **Add New Application Password**
6. Copy the generated password (shown once)

## References

- `references/industry-keywords.md` - Comprehensive keyword lists by industry
- `references/locations.md` - West Yorkshire towns and areas for local SEO

## Error Handling

- Skip unreadable images (log to stderr)
- Handle duplicate names by appending `-2`, `-3`, etc.
- Validate WordPress credentials before starting upload
- Create backup if `--backup` flag used
