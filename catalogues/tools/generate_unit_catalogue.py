"""Generate the offline unit catalogue from the pinned QUDT vocabulary.

Requires rdflib. QUDT vocabulary: CC BY 4.0, https://qudt.org/.
"""
import json
from pathlib import Path
from urllib.request import urlopen

from rdflib import Graph, Namespace, RDF, RDFS, URIRef

SOURCE = "https://raw.githubusercontent.com/qudt/qudt-public-repo/v3.5.2/src/main/rdf/vocab/unit/VOCAB_QUDT-UNITS-ALL.ttl"
QUDT = Namespace("http://qudt.org/schema/qudt/")
UNIT = "http://qudt.org/vocab/unit/"


def main():
    with urlopen(SOURCE, timeout=60) as response:
        data = response.read()
    graph = Graph().parse(data=data, format="turtle")
    units = []
    for subject in set(graph.subjects(RDF.type, QUDT.Unit)):
        if not isinstance(subject, URIRef) or not str(subject).startswith(UNIT):
            continue
        if any(str(value).lower() in {"true", "1"} for value in graph.objects(subject, QUDT.deprecated)):
            continue
        symbols = sorted({str(value) for value in graph.objects(subject, QUDT.symbol) if str(value).strip()})
        codes = sorted({str(value) for value in graph.objects(subject, QUDT.ucumCode) if str(value).strip()})
        labels = sorted({str(value) for value in graph.objects(subject, RDFS.label) if getattr(value, "language", None) in (None, "en", "en-US") and str(value).strip()})
        if not labels or not (symbols or codes):
            continue
        kinds = sorted({str(value).rsplit('/', 1)[-1] for predicate in (QUDT.hasQuantityKind, QUDT.unitForQuantityKind) for value in graph.objects(subject, predicate)})
        units.append({"identifier": str(subject), "symbol": (symbols or codes)[0], "name": labels[0], "quantities": kinds, "aliases": sorted(set(symbols + codes))})
    units.sort(key=lambda unit: unit["identifier"])
    target = Path(__file__).resolve().parents[1] / "qudt-units-3.5.2.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(units, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f"Wrote {len(units)} units to {target}")


if __name__ == "__main__":
    main()
