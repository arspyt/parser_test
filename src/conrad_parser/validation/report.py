import logging
from collections import Counter

from conrad_parser.models import ProductRow

log = logging.getLogger(__name__)


def log_report(rows: list[ProductRow]) -> None:
    counts = Counter(i.split(":")[0] if i.startswith("no_spec") else i
                     for r in rows for i in r.validation_issues)
    clean = sum(1 for r in rows if not r.validation_issues)
    lines = [f"Validation: {clean}/{len(rows)} rows without issues"]
    lines += [f"  {k}: {n}" for k, n in counts.most_common()]
    log.info("\n".join(lines))
