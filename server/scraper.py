import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Base documentation URLs
CDP_DOCS = {
    "segment": "https://segment.com/docs/guides/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

def setup_selenium():
    """Initializes Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_all_links(driver, base_url):
    """Finds all internal documentation links from the main page."""
    driver.get(base_url)
    time.sleep(5)  # Allow JavaScript to load
    
    links = set()
    elements = driver.find_elements(By.TAG_NAME, "a")
    
    for elem in elements:
        href = elem.get_attribute("href")
        if href and href.startswith(base_url) and "docs" in href:  # Filter only docs links
            links.add(href)

    # Debug: Print extracted links
    print(f"Extracted {len(links)} links from {base_url}:")
    for link in links:
        print(link)

    return list(links)


def scrape_page(driver, url):
    """Fetches useful text from a dynamically loaded page."""
    driver.get(url)
    time.sleep(10)  # Give JavaScript more time to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract documentation content (skip menu and headers)
    content_sections = soup.find_all(["p", "h2", "h3", "h4", "li", "pre", "code"])
    paragraphs = [p.get_text(strip=True) for p in content_sections if p.get_text(strip=True) and len(p.get_text(strip=True).split()) > 5]

    return "\n".join(paragraphs)


def fetch_full_documentation(cdp_name):
    """Scrapes all pages from the documentation and stores them locally."""
    if cdp_name not in CDP_DOCS:
        return f"CDP '{cdp_name}' not found. Choose from {list(CDP_DOCS.keys())}"

    driver = setup_selenium()
    base_url = CDP_DOCS[cdp_name]
    
    print(f"Fetching links from {base_url}...")
    links = get_all_links(driver, base_url)
    print(f"Found {len(links)} documentation pages.")

    full_content = []
    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping: {link}")
        content = scrape_page(driver, link)
        if content:
            full_content.append(content)

    driver.quit()

    file_path = f"data/{cdp_name}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(full_content))

    return f"Fetched and saved full documentation for {cdp_name}."

# Example usage:
if __name__ == "__main__":
    for cdp in CDP_DOCS:
        print(fetch_full_documentation(cdp))