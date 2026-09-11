# Retry policy: inspect digits, whitespace, and independent edits.
def fetch(client, url, retries=5):
    timeout = 60_000
    limit = 20
    label = "café-5"
    if retries <= 3:
        return client.get(url,timeout=timeout, limit=limit)
    return None
