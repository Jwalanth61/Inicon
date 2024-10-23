import argparse
import requests
import subprocess
import os
import asyncio
import aiohttp
import subprocess

# Function to print the tool banner using figlet
def print_banner():
    try:
        subprocess.run(["figlet", "Inicon"], check=True)
        print("Inicon - Initial Recon Tool")
    except FileNotFoundError:
        print("(Install figlet for enhanced banners)")

# Function for Subdomain Enumeration using subfinder
def subdomain_enum(domain, verbose=False):
    """Perform subdomain enumeration using subfinder."""
    if verbose:
        print(f"[*] Starting subdomain enumeration for {domain}")

    try:
        # Run subfinder as a subprocess to find subdomains
        result = subprocess.run(['subfinder', '-d', domain, '-silent'], capture_output=True, text=True)
        subdomains = result.stdout.splitlines()
        if verbose:
            print(f"[+] Subdomain enumeration completed. Found {len(subdomains)} subdomains.")
    except Exception as e:
        print(f"Error during subdomain enumeration: {str(e)}")
        return []

    return subdomains

# Asynchronous function to check for live subdomains
async def check_single_subdomain(subdomain, verbose):
    """Check if a single subdomain is live."""
    url = f"https://{subdomain}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:  # Increased timeout
                if response.status == 200:
                    print(f"[+] {subdomain} is live!")
                    return subdomain
                else:
                    print(f"[-] {subdomain} returned status code {response.status}")
                    return None
        except asyncio.TimeoutError:
            print(f"[-] Timeout occurred while checking {subdomain}.")
            return None
        except Exception as e:
            print(f"[-] Error occurred while checking {subdomain}: {e}")
            return None

async def check_live_subdomains(subdomains, verbose=False):
    """Check which found subdomains are live."""
    live_urls = []
    not_live_urls = []
    
    semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent requests

    async def check_with_semaphore(subdomain):
        async with semaphore:
            result = await check_single_subdomain(subdomain, verbose)
            if result:
                live_urls.append(result)
            else:
                not_live_urls.append(subdomain)

    tasks = [check_with_semaphore(subdomain) for subdomain in subdomains]
    await asyncio.gather(*tasks)

    return live_urls, not_live_urls

def run_check_live_subdomains(subdomains, verbose=False):
    """Wrapper to run the async function in the event loop."""
    return asyncio.run(check_live_subdomains(subdomains, verbose))

# Function to check for metafiles on live URLs
def check_metafiles(live_urls):
    """Check for the presence of specific metafiles on live URLs."""
    metafiles = ['robots.txt', 'security.txt', 'sitemap.xml', 'humans.txt', '.well-known/security.txt']
    found_metafiles = []

    for url in live_urls:
        for metafile in metafiles:
            full_url = f"https://{url}/{metafile}"
            try:
                response = requests.get(full_url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Found metafile: {full_url}")
                    found_metafiles.append(full_url)
                else:
                    print(f"[-] Metafile {metafile} not found at {full_url} (status code: {response.status_code})")
            except requests.ConnectionError:
                print(f"[-] Connection error while checking {full_url}.")

    return found_metafiles

# Help menu description
def create_parser():
    parser = argparse.ArgumentParser(
        description="Inicon - Initial Recon Tool for Subdomain Enumeration, Live Subdomains, and Metafiles lookup"
    )
    parser.add_argument('-d', '--domain', help='Specify the domain for recon', required=True)
    parser.add_argument('--subenum', action='store_true', help='Perform Subdomain Enumeration using subfinder')
    parser.add_argument('--livesub', action='store_true', help='Check live subdomains')
    parser.add_argument('--metafiles', action='store_true', help='Find specific metafiles on live subdomains')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    # Adding example commands to the help menu
    parser.epilog = (
        "Examples:\n"
        "  Perform subdomain enumeration:\n"
        "    python3 inicon.py -d example.com --subenum\n"
        "\n"
        "  Check live subdomains after enumeration:\n"
        "    python3 inicon.py -d example.com --livesub\n"
        "\n"
        "  Check for metafiles on live subdomains:\n"
        "    python3 inicon.py -d example.com --subenum --livesub --metafiles\n"
        "\n"
        "  Perform all functions at once:\n"
        "    python3 inicon.py -d example.com --subenum --livesub --metafiles\n"
    )

    return parser

# Main function to run the tool
def main():
    print_banner()  # Display banner at start

    parser = create_parser()
    args = parser.parse_args()

    # If no flags are provided, print help
    if not any(vars(args).values()):
        parser.print_help()
        exit()

    # Subdomain Enumeration
    if args.subenum:
        print("\n--------------------------------------------")
        print("Subdomain enumeration")
        print("--------------------------------------------")
        subdomains = subdomain_enum(args.domain, args.verbose)
        print("\n[*] Found subdomains:")
        print("--------------------------------------------")
        for sub in subdomains:
            print(f"[+] {sub}")
        print("--------------------------------------------\n")

    # Check for Live Subdomains
    if args.livesub:
        print("\n--------------------------------------------")
        print("Live hosts")
        print("--------------------------------------------")
        if 'subdomains' in locals():
            live_urls, not_live_urls = run_check_live_subdomains(subdomains, args.verbose)
            print(f"\n[*] Live URLs:")
            print("--------------------------------------------")
            for live in live_urls:
                print(f"[+] {live}")
            print("\n[*] Not Live URLs:")
            print("--------------------------------------------")
            for not_live in not_live_urls:
                print(f"[-] {not_live}")
            print("--------------------------------------------\n")

            # Check for Metafiles on Live URLs
            if args.metafiles:
                print("\n--------------------------------------------")
                print("Metafile")
                print("--------------------------------------------")
                print(f"[*] Checking for metafiles on live URLs...")
                check_metafiles(live_urls)
                print("--------------------------------------------")
        else:
            print("Error: Please perform subdomain enumeration first using --subenum.")

if __name__ == "__main__":
    main()
