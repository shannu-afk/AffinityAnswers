import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import sys

def search_mdcomputers(search_term):
    """
    Search for products on MDComputers.in with fallback strategies.
    """
    encoded_search = urllib.parse.quote_plus(search_term)
    url = f"https://mdcomputers.in/index.php?route=product/search&search={encoded_search}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Strategy 1: Look for product links
    products = []
    
    # Find all links that contain "/product/" in href - these are likely product links
    product_links = soup.find_all('a', href=True)
    product_links = [link for link in product_links if '/product/' in link['href']]
    
    print(f"Found {len(product_links)} potential product links")
    
    for link in product_links:
        product_name = link.get_text(strip=True)
        product_url = urllib.parse.urljoin("https://mdcomputers.in/", link['href'])
        
        # Skip if name is too short or looks like UI text
        if (not product_name or 
            len(product_name) < 5 or
            re.search(r'Quick View|Compare|Add to|View|Cart|-?\d+%|^[0-9]+$', product_name, re.IGNORECASE)):
            continue
            
        # Find the parent container to extract price
        parent = link.find_parent()
        price = "N/A"
        regular_price = None
        
        # Search for price in the parent and its siblings
        price_text = ""
        current = parent
        for _ in range(10):  # Search up to 10 levels up
            if current and hasattr(current, 'get_text'):
                text = current.get_text()
                if '₹' in text:
                    price_text = text
                    break
                current = current.parent
            else:
                break
        
        if price_text:
            # Extract prices
            prices = re.findall(r'₹[\d,]+', price_text)
            if len(prices) >= 2:
                regular_price = prices[0]
                price = prices[1]
            elif len(prices) == 1:
                price = prices[0]
        
        # Try to find stock info
        stock_status = "Unknown"
        stock_text = ""
        current = parent
        for _ in range(5):
            if current and hasattr(current, 'get_text'):
                text = current.get_text().lower()
                if 'stock' in text or 'availability' in text:
                    stock_text = current.get_text(strip=True)
                    break
                current = current.parent
        
        if stock_text:
            stock_status = stock_text
        elif 'in stock' in response.text.lower():
            stock_status = "In Stock"
        
        products.append({
            'name': product_name,
            'price': price,
            'regular_price': regular_price,
            'stock_status': stock_status,
            'url': product_url
        })
    
    # Remove duplicates
    seen_names = set()
    unique_products = []
    for p in products:
        if p['name'] not in seen_names:
            seen_names.add(p['name'])
            unique_products.append(p)
    
    return unique_products

def display_products(products):
    if not products:
        print("❌ No valid products found.")
        return

    def truncate_name(name, max_len=50):
        return (name[:max_len - 3] + '...') if len(name) > max_len else name

    print(f"\n✅ Found {len(products)} products:\n")
    
    for i, p in enumerate(products, 1):
        name = truncate_name(p['name'])
        price = p['price']
        stock = p['stock_status']
        print(f"{i:2}. {name}")
        print(f"    Price: {price}")
        if p['regular_price']:
            print(f"    Was: {p['regular_price']}")
        print(f"    Stock: {stock}")
        print(f"    URL: {p['url']}\n")

def main():
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
    else:
        search_term = input("Enter a product to search for on MDComputers: ").strip()
    
    if not search_term:
        print("⚠️ Empty search term.")
        return

    print(f"\n🔍 Searching for: '{search_term}'")
    products = search_mdcomputers(search_term)
    display_products(products)

if __name__ == "__main__":
    main()