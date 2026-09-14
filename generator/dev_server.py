#!/usr/bin/env python3
"""
Development server with auto-rebuild and live reload.

Run from the site directory:
    python ../tills-static-site-generator/dev_server.py
"""

import argparse
import os
import socket
import sys
from pathlib import Path
from livereload import Server

# Add site directory (cwd) to path for config import
sys.path.insert(0, os.getcwd())

# Import generator from same directory as this script
generator_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(generator_dir))
import generate_site

# Configuration
HOST = "localhost"
DEFAULT_PORT = 8000
OUTPUT_DIR = "docs"
WATCH_PATHS = ["content", "templates", "static"]
WATCH_FILES = ["design_variables.py", "config.py"]


def find_free_port(start_port=DEFAULT_PORT):
    """Find a free port, starting from start_port."""
    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"Could not find free port in range {start_port}-{start_port + 99}")

# ANSI color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'


def rebuild_site():
    """Rebuild the site."""
    print(f"{Colors.BLUE}  Rebuilding site...{Colors.RESET}")
    try:
        # Reload modules to pick up changes
        import importlib
        import config
        importlib.reload(config)
        importlib.reload(generate_site)

        generate_site.generate_site()
        print(f"{Colors.GREEN}  Rebuild complete!{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.RED}  Rebuild failed: {e}{Colors.RESET}\n")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Development server with live reload.')
    parser.add_argument('-p', '--port', type=int, default=None,
                        help=f'Port to serve on (default: auto-detect starting from {DEFAULT_PORT})')
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Determine port: use specified, or auto-detect
    if args.port:
        port = args.port
    else:
        port = find_free_port()

    # Get site name from config
    try:
        import config
        site_name = getattr(config, 'SITE_NAME', 'Site')
    except ImportError:
        site_name = 'Site'
        print(f"{Colors.RED}Warning: No config.py found in current directory{Colors.RESET}")

    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {site_name} Development Server (Live Reload){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    project_root = os.getcwd()
    serve_dir = os.path.join(project_root, OUTPUT_DIR)

    # Initial build
    print(f"{Colors.BLUE}  Performing initial build...{Colors.RESET}")
    try:
        generate_site.generate_site()
        print(f"{Colors.GREEN}  Initial build complete!{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.RED}  Initial build failed: {e}{Colors.RESET}")
        print(f"{Colors.RED}Please fix the errors and try again.{Colors.RESET}\n")
        sys.exit(1)

    # Create livereload server
    server = Server()

    # Watch directories
    for path in WATCH_PATHS:
        abs_path = os.path.join(project_root, path)
        if os.path.exists(abs_path):
            server.watch(f"{abs_path}/**/*", rebuild_site)
            print(f"{Colors.CYAN}  Watching:{Colors.RESET} {path}/")

    # Watch individual files
    for file in WATCH_FILES:
        abs_path = os.path.join(project_root, file)
        if os.path.exists(abs_path):
            server.watch(abs_path, rebuild_site)
            print(f"{Colors.CYAN}  Watching:{Colors.RESET} {file}")

    print()
    print(f"{Colors.GREEN}  Server running at {Colors.BOLD}http://{HOST}:{port}/{Colors.RESET}")
    print(f"{Colors.CYAN}  Serving files from: {Colors.RESET}{serve_dir}\n")

    # Instructions
    print(f"{Colors.YELLOW}  Tips:{Colors.RESET}")
    print(f"   - Edit files in content/, templates/, or config files")
    print(f"   - Site will automatically rebuild on changes")
    print(f"   - Browser will automatically reload!")
    print(f"   - Press {Colors.BOLD}Ctrl+C{Colors.RESET} to stop\n")

    print(f"{Colors.GREEN}  Development server is ready!{Colors.RESET}")
    print(f"{Colors.CYAN}{'─'*60}{Colors.RESET}\n")

    # Start server (this blocks)
    server.serve(root=serve_dir, host=HOST, port=port)


if __name__ == "__main__":
    main()
