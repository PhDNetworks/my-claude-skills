#!/usr/bin/env python3
"""
WordPress WP-CLI Commands via SSH

Wrapper for executing WP-CLI commands on remote WordPress installations.
"""

import subprocess
import json
import shlex
from pathlib import Path
from typing import Optional, Dict, Any, List


class WordPressClient:
    """WordPress client using SSH and WP-CLI."""

    def __init__(
        self,
        host: str,
        user: str,
        wp_path: str,
        port: int = 22,
        key_path: str = "~/.ssh/id_ed25519"
    ):
        self.host = host
        self.user = user
        self.port = port
        self.key_path = Path(key_path).expanduser()
        self.wp_path = wp_path

    def _ssh_command(self, command: str, timeout: int = 30) -> subprocess.CompletedProcess:
        """Execute command via SSH."""
        ssh_cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=10",
            "-p", str(self.port),
            "-i", str(self.key_path),
            f"{self.user}@{self.host}",
            f"cd {self.wp_path} && {command}"
        ]

        return subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

    def _wp_cli(self, command: str, format_json: bool = False) -> Dict[str, Any]:
        """Execute WP-CLI command."""
        wp_cmd = f"wp {command}"
        if format_json:
            wp_cmd += " --format=json"

        result = self._ssh_command(wp_cmd)

        if result.returncode != 0:
            raise RuntimeError(f"WP-CLI error: {result.stderr}")

        if format_json and result.stdout.strip():
            return json.loads(result.stdout)

        return {"output": result.stdout.strip()}

    # ========== Site Info ==========

    def get_site_info(self) -> Dict[str, Any]:
        """Get basic site information."""
        return {
            "url": self._wp_cli("option get siteurl")["output"],
            "name": self._wp_cli("option get blogname")["output"],
            "wp_version": self._wp_cli("core version")["output"],
        }

    def get_plugins(self, status: str = None) -> List[Dict]:
        """List installed plugins."""
        cmd = "plugin list"
        if status:
            cmd += f" --status={status}"
        return self._wp_cli(cmd, format_json=True)

    def get_theme(self) -> Dict[str, Any]:
        """Get active theme info."""
        themes = self._wp_cli("theme list --status=active", format_json=True)
        return themes[0] if themes else {}

    def is_plugin_active(self, plugin: str) -> bool:
        """Check if a plugin is active."""
        try:
            result = self._wp_cli(f"plugin is-active {plugin}")
            return result.get("output", "") == ""
        except RuntimeError:
            return False

    # ========== Pages ==========

    def create_page(
        self,
        title: str,
        slug: str = None,
        content: str = "",
        status: str = "draft"
    ) -> Dict[str, Any]:
        """Create a new page."""
        cmd = f'post create --post_type=page --post_title="{title}" --post_status={status}'
        if slug:
            cmd += f' --post_name="{slug}"'
        if content:
            # Escape content for shell
            escaped_content = shlex.quote(content)
            cmd += f' --post_content={escaped_content}'
        cmd += " --porcelain"  # Return just the ID

        result = self._ssh_command(f"wp {cmd}")
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create page: {result.stderr}")

        page_id = result.stdout.strip()
        return {"page_id": int(page_id)}

    def get_pages(self, fields: List[str] = None) -> List[Dict]:
        """List all pages."""
        cmd = "post list --post_type=page"
        if fields:
            cmd += f" --fields={','.join(fields)}"
        return self._wp_cli(cmd, format_json=True)

    def get_page(self, page_id: int) -> Dict[str, Any]:
        """Get page details."""
        return self._wp_cli(f"post get {page_id}", format_json=True)

    def update_page(self, page_id: int, **kwargs) -> Dict[str, Any]:
        """Update page properties."""
        cmd = f"post update {page_id}"
        for key, value in kwargs.items():
            cmd += f' --{key}="{value}"'
        return self._wp_cli(cmd)

    def get_page_url(self, page_id: int) -> str:
        """Get the URL for a page."""
        result = self._wp_cli(f"post list --post__in={page_id} --field=url")
        return result.get("output", "")

    # ========== Meta ==========

    def update_meta(self, post_id: int, key: str, value: str) -> Dict[str, Any]:
        """Update post meta."""
        escaped_value = shlex.quote(value)
        return self._wp_cli(f"post meta update {post_id} {key} {escaped_value}")

    def get_meta(self, post_id: int, key: str = None) -> Any:
        """Get post meta."""
        cmd = f"post meta get {post_id}"
        if key:
            cmd += f" {key}"
        return self._wp_cli(cmd)

    # ========== Elementor ==========

    def import_elementor_template(self, page_id: int, template_data: Dict) -> Dict[str, Any]:
        """Import Elementor template data to a page."""
        # Elementor stores data as post meta
        # Key: _elementor_data (JSON string)
        # Key: _elementor_edit_mode (builder)

        if not self.is_plugin_active("elementor"):
            raise RuntimeError("Elementor is not active on this site")

        # Convert template to JSON string
        template_json = json.dumps(template_data.get("content", []))
        escaped_json = shlex.quote(template_json)

        # Update Elementor meta
        self.update_meta(page_id, "_elementor_data", template_json)
        self.update_meta(page_id, "_elementor_edit_mode", "builder")
        self.update_meta(page_id, "_elementor_template_type", "wp-page")

        return {"success": True, "page_id": page_id}

    # ========== Schema ==========

    def inject_schema(self, page_id: int, schema: Dict) -> Dict[str, Any]:
        """Inject JSON-LD schema into page."""
        # Store schema in custom field
        schema_json = json.dumps(schema, indent=2)
        return self.update_meta(page_id, "_landing_page_schema", schema_json)

    # ========== Users ==========

    def get_users(self, role: str = None) -> List[Dict]:
        """List users."""
        cmd = "user list"
        if role:
            cmd += f" --role={role}"
        return self._wp_cli(cmd, format_json=True)

    # ========== Options ==========

    def get_option(self, name: str) -> str:
        """Get WordPress option."""
        result = self._wp_cli(f"option get {name}")
        return result.get("output", "")

    def update_option(self, name: str, value: str) -> Dict[str, Any]:
        """Update WordPress option."""
        return self._wp_cli(f'option update {name} "{value}"')


# Convenience functions for direct use

def discover_site(host: str, user: str, wp_path: str, port: int = 22) -> Dict[str, Any]:
    """Discover WordPress site configuration."""
    wp = WordPressClient(host=host, user=user, wp_path=wp_path, port=port)

    site_info = wp.get_site_info()
    plugins = wp.get_plugins(status="active")
    theme = wp.get_theme()
    pages = wp.get_pages(fields=["ID", "post_title", "post_name"])
    admins = wp.get_users(role="administrator")

    return {
        "site": site_info,
        "theme": theme,
        "active_plugins": [p["name"] for p in plugins],
        "has_elementor": wp.is_plugin_active("elementor"),
        "pages": pages,
        "admins": [{"id": u["ID"], "login": u["user_login"]} for u in admins]
    }


if __name__ == "__main__":
    # Test connection
    import sys

    if len(sys.argv) < 4:
        print("Usage: python wp_cli_commands.py <host> <user> <wp_path> [port]")
        sys.exit(1)

    host = sys.argv[1]
    user = sys.argv[2]
    wp_path = sys.argv[3]
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 22

    print(f"Discovering site: {host}...")
    try:
        config = discover_site(host, user, wp_path, port)
        print(json.dumps(config, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
