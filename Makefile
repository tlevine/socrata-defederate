.PHONY: download
download:
		./download.sh

json: download
		./federation.py > federation.json

dcat: download
		./dedupe.py json

csv: download
		./dedupe.py csv
