import tldextract

def check_domain(url):
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"

        if len(domain) > 25:
            return 7, "long_domain"

        if any(x in domain for x in ["loan", "win", "offer"]):
            return 6, "suspicious_keyword_domain"

        if domain.endswith(".xyz") or domain.endswith(".top"):
            return 7, "low_trust_tld"

        return 2, "normal_domain"

    except:
        return 5, "unknown_domain"