#!/usr/bin/env python3
"""
ImageForge Pro - Professional image optimization for web projects.
Unified script handling rename, EXIF embedding, and WordPress upload.
"""

import os
import sys
import csv
import argparse
import shutil
from datetime import datetime
from pathlib import Path

# Supported image extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def get_images(folder: str) -> list:
    """Get all supported images in folder."""
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"Error: Folder not found: {folder}", file=sys.stderr)
        sys.exit(1)
    
    images = []
    for f in folder_path.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append({
                'path': str(f),
                'filename': f.name,
                'extension': f.suffix.lower(),
                'size': f.stat().st_size
            })
    
    return sorted(images, key=lambda x: x['filename'])


def list_images(folder: str, industry: str = None) -> None:
    """List all images in folder."""
    images = get_images(folder)
    
    if not images:
        print(f"No supported images found in {folder}")
        print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        return
    
    print(f"\n📁 Found {len(images)} images in {folder}")
    if industry:
        print(f"🏷️  Industry context: {industry}")
    print("-" * 60)
    
    total_size = 0
    for img in images:
        size_kb = img['size'] / 1024
        total_size += img['size']
        print(f"  {img['filename']:<40} {size_kb:>8.1f} KB")
    
    print("-" * 60)
    print(f"  Total: {len(images)} files, {total_size/1024/1024:.1f} MB")


def generate_template(folder: str, output_file: str = None) -> str:
    """Generate CSV template for batch editing."""
    images = get_images(folder)
    
    if not images:
        print(f"No images found in {folder}", file=sys.stderr)
        sys.exit(1)
    
    output_file = output_file or os.path.join(folder, 'imageforge_template.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'original_filename', 'new_filename', 'alt_text', 'title'
        ])
        writer.writeheader()
        for img in images:
            writer.writerow({
                'original_filename': img['filename'],
                'new_filename': '',  # To be filled in by Claude or user
                'alt_text': '',      # To be filled in
                'title': ''          # To be filled in
            })
    
    print(f"✅ Template generated: {output_file}")
    print(f"   Fill in new_filename, alt_text, and title columns")
    return output_file


def write_manifest(folder: str, results: list) -> str:
    """Write processing manifest CSV."""
    manifest_file = os.path.join(folder, 'imageforge_manifest.csv')
    
    with open(manifest_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'original_filename', 'new_filename', 'alt_text', 'title', 
            'status', 'timestamp'
        ])
        writer.writeheader()
        for result in results:
            writer.writerow({
                'original_filename': result.get('old_name', ''),
                'new_filename': result.get('new_name', ''),
                'alt_text': result.get('alt_text', ''),
                'title': result.get('title', ''),
                'status': 'success' if result.get('success') else 'failed',
                'timestamp': datetime.now().isoformat()
            })
    
    return manifest_file


def rename_image(folder: str, old_name: str, new_name: str, 
                 location: str = None, dry_run: bool = False,
                 backup: bool = False) -> dict:
    """Rename a single image file."""
    old_path = Path(folder) / old_name
    
    if not old_path.exists():
        return {'success': False, 'error': f'File not found: {old_name}'}
    
    # Build new filename
    ext = old_path.suffix.lower()
    base_name = new_name.lower().replace(' ', '-').replace('_', '-')
    
    # Append location if provided and not already in name
    if location and location.lower() not in base_name:
        base_name = f"{base_name}-{location.lower()}"
    
    # Ensure extension
    if not base_name.endswith(ext):
        base_name = f"{base_name}{ext}"
    
    new_path = Path(folder) / base_name
    
    # Handle duplicates
    counter = 2
    original_base = base_name.replace(ext, '')
    while new_path.exists() and new_path != old_path:
        base_name = f"{original_base}-{counter}{ext}"
        new_path = Path(folder) / base_name
        counter += 1
    
    if dry_run:
        return {
            'success': True,
            'old_name': old_name,
            'new_name': base_name,
            'dry_run': True
        }
    
    try:
        if backup:
            shutil.copy2(old_path, str(old_path) + '.bak')
        
        old_path.rename(new_path)
        return {
            'success': True,
            'old_name': old_name,
            'new_name': base_name
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def embed_exif(image_path: str, alt_text: str, dry_run: bool = False) -> dict:
    """Embed alt text into JPEG EXIF metadata."""
    try:
        import piexif
    except ImportError:
        return {
            'success': False,
            'error': 'piexif not installed. Run: pip install piexif'
        }
    
    path = Path(image_path)
    if path.suffix.lower() not in {'.jpg', '.jpeg'}:
        return {
            'success': False,
            'error': 'EXIF embedding only supported for JPEG files'
        }
    
    if dry_run:
        return {
            'success': True,
            'path': str(path),
            'alt_text': alt_text,
            'dry_run': True
        }
    
    try:
        # Load existing EXIF or create new
        try:
            exif_dict = piexif.load(str(path))
        except:
            exif_dict = {'0th': {}, '1st': {}, 'Exif': {}, 'GPS': {}, 'Interop': {}}
        
        # Set ImageDescription (alt text)
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = alt_text.encode('utf-8')
        
        # Write back
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, str(path))
        
        return {
            'success': True,
            'path': str(path),
            'alt_text': alt_text
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def upload_to_wordpress(image_path: str, alt_text: str, title: str,
                        site_url: str, username: str, password: str,
                        dry_run: bool = False) -> dict:
    """Upload image to WordPress via REST API."""
    try:
        import requests
    except ImportError:
        return {
            'success': False,
            'error': 'requests not installed. Run: pip install requests'
        }
    
    path = Path(image_path)
    
    if dry_run:
        return {
            'success': True,
            'path': str(path),
            'site': site_url,
            'dry_run': True
        }
    
    # Normalize site URL
    site_url = site_url.rstrip('/')
    api_url = f"{site_url}/wp-json/wp/v2/media"
    
    try:
        # Read file
        with open(path, 'rb') as f:
            file_data = f.read()
        
        # Determine content type
        ext = path.suffix.lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        
        # Upload
        headers = {
            'Content-Disposition': f'attachment; filename="{path.name}"',
            'Content-Type': content_type
        }
        
        response = requests.post(
            api_url,
            headers=headers,
            data=file_data,
            auth=(username, password),
            timeout=60
        )
        
        if response.status_code not in [200, 201]:
            return {
                'success': False,
                'error': f'Upload failed: {response.status_code} - {response.text}'
            }
        
        media_id = response.json().get('id')
        
        # Update alt text and title
        update_url = f"{api_url}/{media_id}"
        update_data = {
            'alt_text': alt_text,
            'title': title,
            'caption': alt_text  # Use alt text as caption too
        }
        
        update_response = requests.post(
            update_url,
            json=update_data,
            auth=(username, password),
            timeout=30
        )
        
        return {
            'success': True,
            'path': str(path),
            'media_id': media_id,
            'url': response.json().get('source_url')
        }
        
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Request failed: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def process_from_csv(folder: str, csv_file: str, mode: str,
                     location: str = None, dry_run: bool = False,
                     backup: bool = False, wp_site: str = None,
                     wp_user: str = None, wp_password: str = None) -> list:
    """Process images from a CSV file."""
    results = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_name = row['original_filename']
            new_name = row.get('new_filename', '').strip()
            alt_text = row.get('alt_text', '').strip()
            title = row.get('title', '').strip()
            
            if not new_name:
                results.append({
                    'old_name': old_name,
                    'success': False,
                    'error': 'No new filename specified'
                })
                continue
            
            # Step 1: Rename
            rename_result = rename_image(folder, old_name, new_name, 
                                         location, dry_run, backup)
            
            if not rename_result.get('success'):
                results.append(rename_result)
                continue
            
            result = rename_result.copy()
            result['alt_text'] = alt_text
            result['title'] = title or new_name.replace('-', ' ').title()
            
            new_path = os.path.join(folder, rename_result['new_name'])
            
            # Step 2: Mode-specific processing
            if mode == 'embed' and alt_text:
                embed_result = embed_exif(new_path, alt_text, dry_run)
                result['embed_success'] = embed_result.get('success')
                if not embed_result.get('success'):
                    result['embed_error'] = embed_result.get('error')
            
            elif mode == 'wordpress' and wp_site:
                upload_result = upload_to_wordpress(
                    new_path, alt_text, result['title'],
                    wp_site, wp_user, wp_password, dry_run
                )
                result['upload_success'] = upload_result.get('success')
                result['media_id'] = upload_result.get('media_id')
                result['url'] = upload_result.get('url')
                if not upload_result.get('success'):
                    result['upload_error'] = upload_result.get('error')
            
            results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='ImageForge Pro - Professional image optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List images in folder
  %(prog)s /path/to/images --list
  
  # Generate CSV template
  %(prog)s /path/to/images --template
  
  # Rename only (after Claude fills in CSV)
  %(prog)s /path/to/images --mode rename --from-csv imageforge_template.csv
  
  # Rename + EXIF embed
  %(prog)s /path/to/images --mode embed --from-csv imageforge_template.csv
  
  # WordPress upload
  %(prog)s /path/to/images --mode wordpress --from-csv imageforge_template.csv \\
    --wp-site https://example.com --wp-user admin --wp-password "xxxx xxxx"
        """
    )
    
    parser.add_argument('folder', help='Path to image folder')
    parser.add_argument('--list', action='store_true', 
                        help='List images in folder')
    parser.add_argument('--template', action='store_true',
                        help='Generate CSV template for batch editing')
    parser.add_argument('--mode', choices=['rename', 'embed', 'wordpress'],
                        default='rename', help='Processing mode')
    parser.add_argument('--industry', help='Industry context for keywords')
    parser.add_argument('--location', help='Location suffix for local SEO')
    parser.add_argument('--from-csv', dest='csv_file',
                        help='Process from CSV file')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview without making changes')
    parser.add_argument('--backup', action='store_true',
                        help='Keep original files with .bak extension')
    
    # WordPress options
    parser.add_argument('--wp-site', help='WordPress site URL')
    parser.add_argument('--wp-user', help='WordPress username')
    parser.add_argument('--wp-password', help='WordPress application password')
    
    args = parser.parse_args()
    
    # Handle --list
    if args.list:
        list_images(args.folder, args.industry)
        return
    
    # Handle --template
    if args.template:
        generate_template(args.folder)
        return
    
    # Process from CSV
    if args.csv_file:
        if not os.path.exists(args.csv_file):
            print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
            sys.exit(1)
        
        # Validate WordPress credentials if needed
        if args.mode == 'wordpress':
            if not all([args.wp_site, args.wp_user, args.wp_password]):
                print("Error: WordPress mode requires --wp-site, --wp-user, "
                      "and --wp-password", file=sys.stderr)
                sys.exit(1)
        
        print(f"\n🔄 Processing images from {args.csv_file}")
        print(f"   Mode: {args.mode}")
        if args.dry_run:
            print("   ⚠️  DRY RUN - no changes will be made")
        print()
        
        results = process_from_csv(
            args.folder, args.csv_file, args.mode,
            args.location, args.dry_run, args.backup,
            args.wp_site, args.wp_user, args.wp_password
        )
        
        # Summary
        success_count = sum(1 for r in results if r.get('success'))
        fail_count = len(results) - success_count
        
        print(f"\n{'Would process' if args.dry_run else 'Processed'} "
              f"{success_count} images" +
              (f" ({fail_count} failed)" if fail_count else ""))
        
        for result in results:
            if result.get('success'):
                status = "✓"
                if args.mode == 'embed' and result.get('embed_success'):
                    status += " 📝"
                elif args.mode == 'wordpress' and result.get('upload_success'):
                    status += " ☁️"
                print(f"  {status} {result['old_name']} → {result['new_name']}")
            else:
                print(f"  ✗ {result.get('old_name', 'Unknown')}: "
                      f"{result.get('error', 'Unknown error')}", file=sys.stderr)
        
        # Write manifest
        if not args.dry_run and success_count > 0:
            manifest = write_manifest(args.folder, results)
            print(f"\n📋 Manifest written: {manifest}")
        
        sys.exit(0 if fail_count == 0 else 1)
    
    # No action specified
    parser.print_help()


if __name__ == '__main__':
    main()
