
def extract_domain(url):
    """Extracts the clean domain name from a URL string"""
    
    
    clean_url = url.strip()
    
    
    if clean_url.startswith("https://"):
        clean_url = clean_url[8:]
    elif clean_url.startswith("http://"):
        clean_url = clean_url[7:]
    
   
    if clean_url.startswith("www."):
        clean_url = clean_url[4:]
    
    
    delimiters = ["/", "?", ":", "#"]
    domain = ""
    
    for ch in clean_url:
        if ch in delimiters:
            break
        domain = domain + ch
    
    return domain
  
