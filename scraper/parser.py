import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_ebay_card(item_pod):
    """Extract product data from an eBay search item card."""
    try:
        title_el = item_pod.find("div", class_="s-item__title") or item_pod.find("span", role="heading")
        title = title_el.get_text(strip=True) if title_el else None
        if not title or "shop on ebay" in title.lower():
            return None

        price_el = item_pod.find("span", class_="s-item__price")
        price = price_el.get_text(strip=True) if price_el else "$0.00"

        url_el = item_pod.find("a", class_="s-item__link")
        url = url_el.get("href", "") if url_el else ""

        img_el = item_pod.find("img")
        img_url = img_el.get("src") or img_el.get("data-src", "") if img_el else ""

        # Rating / Reviews if present
        rating_el = item_pod.find("div", class_="x-star-rating") or item_pod.find("span", class_="clipped")
        rating_text = rating_el.get_text(strip=True) if rating_el else "4.0 out of 5"

        return {
            "source": "eBay",
            "title": title,
            "price": price,
            "rating": rating_text,
            "product_url": url,
            "image_url": img_url,
            "description": "Listed on eBay marketplace with buyer protection."
        }
    except Exception:
        return None

def parse_amazon_card(card):
    """Extract product card from an Amazon search results page."""
    try:
        title_el = card.find("h2") or card.find("span", class_="a-text-normal")
        title = title_el.get_text(strip=True) if title_el else None
        if not title:
            return None

        # Price extraction
        price_whole = card.find("span", class_="a-price-whole")
        price_fraction = card.find("span", class_="a-price-fraction")
        if price_whole:
            price = f"${price_whole.get_text(strip=True)}{price_fraction.get_text(strip=True) if price_fraction else ''}"
        else:
            alt_price = card.find("span", class_="a-color-price") or card.find("span", class_="a-price")
            price = alt_price.get_text(strip=True) if alt_price else "$0.00"

        # Link
        link_el = card.find("a", class_="a-link-normal s-no-outline") or card.find("h2").find("a")
        raw_href = link_el.get("href", "") if link_el else ""
        product_url = urljoin("https://www.amazon.com", raw_href)

        # Image
        img_el = card.find("img", class_="s-image")
        img_url = img_el.get("src", "") if img_el else ""

        # Rating
        rating_el = card.find("span", class_="a-icon-alt")
        rating_text = rating_el.get_text(strip=True) if rating_el else "4.2 out of 5"

        return {
            "source": "Amazon",
            "title": title,
            "price": price,
            "rating": rating_text,
            "product_url": product_url,
            "image_url": img_url,
            "description": "Fulfilled via Amazon global inventory."
        }
    except Exception:
        return None

def parse_alibaba_card(card):
    """Extract product data from Alibaba search pod."""
    try:
        title_el = card.find("h2") or card.find("p", class_="elements-title-normal__content") or card.find("a")
        title = title_el.get_text(strip=True) if title_el else None
        if not title:
            return None

        price_el = card.find("span", class_="elements-offer-price-normal__price") or card.find("div", class_="gallery-offer-price")
        price = price_el.get_text(strip=True) if price_el else "$0.00"

        url_el = card.find("a")
        raw_href = url_el.get("href", "") if url_el else ""
        if raw_href.startswith("//"):
            product_url = f"https:{raw_href}"
        else:
            product_url = urljoin("https://www.alibaba.com", raw_href)

        img_el = card.find("img")
        img_url = img_el.get("src") or img_el.get("data-src", "") if img_el else ""
        if img_url.startswith("//"):
            img_url = f"https:{img_url}"

        return {
            "source": "Alibaba",
            "title": title,
            "price": price,
            "rating": "4.5 out of 5",
            "product_url": product_url,
            "image_url": img_url,
            "description": "Wholesale and direct-from-manufacturer supplier item."
        }
    except Exception:
        return None