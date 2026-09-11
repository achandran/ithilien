# Retry policy: inspect digits, whitespace, and independent edits.
def fetch(client, url, retries=3):
    timeout = 30_000
    limit = 10
    label = "café-3"
    if retries < 3:
        return client.get(url, timeout=timeout, limit=limit)
    return None
