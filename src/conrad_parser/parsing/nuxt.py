"""Nuxt SSR state (<script id="__NUXT_DATA__">) serialized with devalue."""
import json
import re
from collections.abc import Callable, Iterator
from typing import Any

_NUXT_DATA_RE = re.compile(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)
_WRAPPERS = {"Reactive", "Ref", "ShallowRef", "ShallowReactive", "EmptyRef",
             "EmptyShallowRef", "skipHydrate"}


def extract_nuxt_payload(html: str) -> list | None:
    m = _NUXT_DATA_RE.search(html)
    return json.loads(m.group(1)) if m else None


def unflatten(data: list) -> Any:
    """devalue format: object/array values are indexes into one shared list."""
    cache: dict[int, Any] = {}

    def res(i):
        if i is None or i == -1:
            return None
        if i in cache:
            return cache[i]
        v = data[i]
        if isinstance(v, list):
            if v and isinstance(v[0], str):          # [tag, reference]
                out = res(v[1]) if (len(v) == 2 and isinstance(v[1], int)
                                    and v[0] in _WRAPPERS) else None
                cache[i] = out
                return out
            out = []
            cache[i] = out
            out.extend(res(j) for j in v)
        elif isinstance(v, dict):
            out = {}
            cache[i] = out
            for k, j in v.items():
                out[k] = res(j)
        else:
            cache[i] = v
        return cache[i]

    return res(0)


def walk(obj: Any, pred: Callable[[dict], bool], path: str = "") -> Iterator[tuple[str, dict]]:
    if isinstance(obj, dict):
        if pred(obj):
            yield path, obj
        for k, v in obj.items():
            yield from walk(v, pred, f"{path}/{k}")
    elif isinstance(obj, list):
        for n, v in enumerate(obj):
            yield from walk(v, pred, f"{path}[{n}]")


def find_with_key(obj: Any, key: str) -> dict | None:
    """The first dict in the tree that contains `key`."""
    return next((o for _, o in walk(obj, lambda o: key in o)), None)
