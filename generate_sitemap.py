import requests
import xml.etree.ElementTree as ET

SITEMAP_URL = "https://docs.myq-solution.com/sitemap.xml"
OUTPUT_FILE = "sitemap-en.xml"

def fetch_sitemap(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def filter_english_sitemaps(xml_text):
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(xml_text)
    en_sitemaps = []

    for sitemap in root.findall("sm:sitemap", ns):
        loc = sitemap.find("sm:loc", ns).text
        if "/en/" in loc:
            en_sitemaps.append(loc)

    return en_sitemaps

def generate_sitemap_xml(urls):
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = ET.Element("sitemapindex", xmlns=ns)
    for url in urls:
        sm = ET.SubElement(root, "sitemap")
        loc = ET.SubElement(sm, "loc")
        loc.text = url
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def main():
    xml_text = fetch_sitemap(SITEMAP_URL)
    en_urls = filter_english_sitemaps(xml_text)
    sitemap_xml = generate_sitemap_xml(en_urls)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(sitemap_xml)

    print(f"English sitemap generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
