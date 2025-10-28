#!/usr/bin/env python3
"""
Rate-limited LinkedIn profile scraper for batch processing
Scrapes profiles with 10-15 second delays to avoid rate limiting
"""

import time
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    return driver

def scrape_linkedin_profile(driver, url, name):
    """Scrape a single LinkedIn profile"""
    try:
        print(f"\n{'='*80}")
        print(f"Scraping: {name}")
        print(f"URL: {url}")
        
        driver.get(url)
        time.sleep(3)  # Let page load
        
        # Try to get headline
        headline = ""
        try:
            headline_elem = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium")
            headline = headline_elem.text.strip()
        except:
            try:
                headline_elem = driver.find_element(By.CLASS_NAME, "top-card-layout__headline")
                headline = headline_elem.text.strip()
            except:
                pass
        
        # Try to get About section
        about = ""
        try:
            about_section = driver.find_element(By.ID, "about")
            about_parent = about_section.find_element(By.XPATH, "..")
            about = about_parent.text.replace("About\n", "").strip()
        except:
            try:
                # Alternative selector
                about_elems = driver.find_elements(By.CSS_SELECTOR, "[class*='about']")
                for elem in about_elems:
                    text = elem.text
                    if len(text) > 100:  # Likely the about section
                        about = text.replace("About\n", "").strip()
                        break
            except:
                pass
        
        result = {
            'name': name,
            'url': url,
            'headline': headline,
            'about': about,
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"✅ Scraped: {name}")
        if headline:
            print(f"   Headline: {headline[:80]}...")
        if about:
            print(f"   About: {len(about)} chars")
        
        return result
        
    except Exception as e:
        print(f"❌ Error scraping {name}: {str(e)}")
        return {
            'name': name,
            'url': url,
            'headline': '',
            'about': '',
            'error': str(e),
            'scraped_at': datetime.now().isoformat()
        }

def main():
    # Read URLs to scrape
    urls_file = Path('integration_scripts/member_enrichment/linkedin_urls_to_scrape.txt')
    
    profiles = []
    with open(urls_file) as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    profiles.append({'name': parts[0], 'url': parts[1]})
    
    print(f"Found {len(profiles)} profiles to scrape")
    print("Starting with 10-15 second delays between requests...")
    
    driver = setup_driver()
    results = []
    
    try:
        for i, profile in enumerate(profiles, 1):
            print(f"\n[{i}/{len(profiles)}]")
            
            result = scrape_linkedin_profile(driver, profile['url'], profile['name'])
            results.append(result)
            
            # Save intermediate results every 5 profiles
            if i % 5 == 0:
                save_results(results, f"_checkpoint_{i}")
            
            # Rate limiting: 10-15 seconds between requests
            if i < len(profiles):
                delay = random.uniform(10, 15)
                print(f"⏳ Waiting {delay:.1f} seconds before next profile...")
                time.sleep(delay)
        
        # Save final results
        save_results(results, "_final")
        
    finally:
        driver.quit()
    
    print("\n" + "="*80)
    print(f"✅ Scraping complete!")
    print(f"   Total profiles: {len(results)}")
    print(f"   Successful: {sum(1 for r in results if r.get('headline') or r.get('about'))}")
    print(f"   Errors: {sum(1 for r in results if r.get('error'))}")

def save_results(results, suffix=""):
    """Save results to markdown file"""
    output_file = Path(f'integration_scripts/member_enrichment/LINKEDIN_PROFILES_BATCH_28{suffix}.md')
    
    with open(output_file, 'w') as f:
        f.write(f"# LinkedIn Profiles - Batch 28\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n")
        f.write(f"**Profiles Scraped:** {len(results)}\n\n")
        f.write("---\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"## {i}. {result['name']}\n\n")
            
            if result.get('headline'):
                f.write(f"**LinkedIn Headline:** {result['headline']}\n\n")
            
            if result.get('about'):
                f.write(f"{result['about']}\n\n")
            elif result.get('error'):
                f.write(f"_[Error: {result['error']}]_\n\n")
            else:
                f.write(f"_[No About section found]_\n\n")
            
            f.write(f"**Source:** {result['url']}\n\n")
            f.write("---\n\n")
    
    print(f"\n💾 Saved: {output_file}")

if __name__ == "__main__":
    main()
