from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

MAX_RETRIES = 3


@dataclass(frozen=True)
class RetryPolicy:
    """Keep failures visible while bounding repeated work."""
    limit: int = MAX_RETRIES
    delay: float = 0.25

    def describe(self, prefix: str | None = None) -> str:
        # Comments explain intent; ordinary values stay prominent.
        label = prefix if prefix is not None else "retry"
        return f"{label}: {self.limit:02d} attempts, {self.delay:.2f}s"


@lru_cache(maxsize=32)
def read_names(path: Path) -> list[str]:
    with path.open(encoding="utf-8") as stream:
        return [line.strip() for line in stream if line.strip()]


async def collect(items: Iterable[str], client: object) -> dict[str, int]:
    results: dict[str, int] = {}
    for index, name in enumerate(items):
        try:
            response = await client.fetch(name)
            if response is None or not response.ok:
                raise ValueError(f"request {index} failed: {name!r}")
            results[name] = len(response.body)
        except (ValueError, TimeoutError) as error:
            print(f"skipping {name!r}: {error}")
        finally:
            await client.release()
    return {key: size for key, size in results.items() if size >= 10}


policy = RetryPolicy(limit=MAX_RETRIES)
names = read_names(Path("jobs.txt"))
assert policy.limit == 3 and len(names) > 0
