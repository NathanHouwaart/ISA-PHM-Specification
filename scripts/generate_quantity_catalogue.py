"""Generate offline QUDT quantity kinds (QUDT 3.5.2, CC BY 4.0)."""
import json
from pathlib import Path
from urllib.request import urlopen

from rdflib import Graph, Namespace, RDF, RDFS, URIRef

SOURCE = 'https://raw.githubusercontent.com/qudt/qudt-public-repo/v3.5.2/src/main/rdf/vocab/quantitykinds/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl'
QUDT = Namespace('http://qudt.org/schema/qudt/')

with urlopen(SOURCE, timeout=60) as response:
    graph = Graph().parse(data=response.read(), format='turtle')
items = []
for subject in set(graph.subjects(RDF.type, QUDT.QuantityKind)):
    if not isinstance(subject, URIRef) or not str(subject).startswith('http://qudt.org/vocab/quantitykind/'):
        continue
    if any(str(value).lower() in {'true', '1'} for value in graph.objects(subject, QUDT.deprecated)):
        continue
    labels = sorted({str(value) for value in graph.objects(subject, RDFS.label) if getattr(value, 'language', None) in (None, 'en', 'en-US') and str(value).strip()})
    if labels:
        items.append({'identifier': str(subject), 'name': labels[0]})
items.sort(key=lambda item: item['identifier'])
target = Path(__file__).resolve().parents[1] / 'catalogues/qudt-quantities-3.5.2.json'
target.write_text(json.dumps(items, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
print(f'Wrote {len(items)} quantity kinds to {target}')
