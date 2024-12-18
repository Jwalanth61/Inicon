# Inicon--Initial_Reconnaissance

## Tool Description

**Inicon** (short for **Initial Recon**) is a command-line reconnaissance tool designed to assist security professionals and enthusiasts in performing initial reconnaissance on domains. Inicon automates essential tasks like subdomain enumeration, live subdomain checks, and metafile enumeration. The tool is built using Python3 and is suitable for penetration testers, red teamers, and cybersecurity analysts who need to gather information about their target domains efficiently.

With Inicon, users can:
- Identify potential subdomains of a given domain using subfinder.
- Verify which of the found subdomains are live (responding).
- Retrieve important metafiles like `robots.txt`, `security.txt`, `sitemap.xml`, `humans.txt`, and `.well-known/security.txt` from live subdomains.

Inicon streamlines the reconnaissance phase of security assessments, making it easier to collect relevant information quickly and effectively.

## Installation Steps

To install Inicon, follow these steps:

1. **Clone the Repository**:
   Open your terminal and clone the repository using the following command:
   
   ```bash
   git clone https://github.com/Jwalanth61/Inicon.git
   
2. **Navigate to the Directory**: Change to the directory where Inicon is located:
   
    ```bash
   cd Inicon
    
3. **Make the Script Executable (optional)**: You can make the script executable by running:
   
   ```bash
   chmod +x inicon.py

## Requirements

To install the required packages and set up a virtual environment, you can use the provided bash script. Follow these steps:

1. **Make the script executable**:
 
   ```bash
   chmod +x install_requirements.sh
   
2. **Run the script**:

   ```bash
   ./install_requirements.sh
   ```
   This will:
   - Check for the installation of Python3, pip, and Subfinder.
   - Create a virtual environment named `myenv`, activate it, and install the necessary packages (`aiohttp` and `requests`).
> If you got an error installing the subfinder, please upgrade the **go** to the latest version using this [link](https://go.dev/doc/install).
   
3. **To activate the virtual environment later, use**:
   ```bash
   source myenv/bin/activate

4. **To deactivate the virtual environment, simply run**:

   ```bash
   deactivate
> For a clear walkthrough of the installation steps, check out [my blog](https://medium.com/@jwalanth/inicon-a-one-stop-recon-tool-for-bug-bounty-hunters-8e1dcfa90a6c).

### Usage

To use Inicon, run the script from the command line with the appropriate flags. The general syntax is as follows:
  
   ```bash
   python3 inicon.py -d <domain> [options]
   ```

## Example Commands

   1. **Perform Initial Reconnaissance**:
  
      ```bash
      python3 inicon.py -d example.com
   
   2. **List Subdomains**:

      ```bash
      python3 inicon.py -d example.com --subenum
      
   3. **List Live Subdomains**:

       ```bash
      python3 inicon.py -d example.com --livesub
       
   4. **List Subdomains with Metafiles**:

       ```bash
      python3 inicon.py -d example.com --metafiles

## Flags Used in the Tool

- `-d, --domain`: Specify the domain to perform reconnaissance on. This flag is **required**.
- `--subenum`: Flag to view subdomain enumeration list.
- `--livesub`: Flag to check and view for live subdomains.
- `--metafiles`: Flag to check for specific metafiles on live subdomains.
- `-w, --wordlist`: Specify the wordlist file to use for subdomain enumeration.
- `-v, --verbose`: Enable verbose output for detailed information during execution.
- `-h, --help`: Show the help message and exit.


### Notes

- Ensure the script has execute permissions (`chmod +x install_requirements.sh`) before running it.

Let me know if you need further adjustments or any additional features!
