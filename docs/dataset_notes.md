# dataset notes

## prvi test sa CICIDS2017 fajlom

- testiran fajl: `data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
- obrađeno je prvih 10000 redova pomoću `--max-rows 10000`
- nakon čišćenja je u izlazu ostalo 9641 redova
- output fajl: `data/processed/ddos_annotated.csv`

## generisani reporti

- `reports/schema_report.json`
- `reports/value_report.json`
- `reports/annotation_summary.json`

## napomena

- ovaj CSV fajl nema `Protocol` kolonu, pa je `protocol` u kodu ostavljen kao opciona kolona
