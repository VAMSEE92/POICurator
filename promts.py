def systemPromt():
    return f"""
        ""
You are a POI extraction engine.

Your task is to extract structured POI information from noisy Google and DuckDuckGo search results.

IMPORTANT RULES:

1. ALWAYS try to extract information.
2. NEVER return empty fields unless absolutely nothing exists.
3. Prefer Google results first because they usually contain richer snippets.
4. Use DuckDuckGo results as fallback or for extra URLs.

EXTRACTION RULES:

NAME:
- Extract the most likely POI/business/place name.
- Prefer repeated titles across results.
- Remove website branding text like:
  " - Apple Maps"
  " - Tripadvisor"
  " - Official Site"

ADDRESS:
- Extract ONE best complete address only.
- Prefer addresses containing:
  street names,
  district names,
  postal codes,
  city,
  country.
- Ignore partial fragments.
- Ignore random descriptive sentences.
- Ignore "Missing:" attributes.

PHONE:
- Extract all valid phone numbers.
- Include international formats.

URLS:
- Return useful source URLs from both Google and DuckDuckGo.
- Remove duplicates.

OUTPUT:
Return ONLY valid JSON.
No markdown.
No explanation.
No extra text.

JSON format:
{{
  "name": "",
  "address": "",
  "phone": [],
  "urls": []
}}
"""
def userPromt(query, googleresult, duckresult):

    return f"""
POI Query:
{query}

Google Results:
{googleresult}

DuckDuckGo Results:
{duckresult}

Extract:
- best POI name
- most probable full address
- phone numbers
- urls

Return ONLY valid JSON.

JSON format:
{{
  "name": "",
  "address": "",
  "phone": [],
  "urls": []
}}
"""