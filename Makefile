.PHONY: download
download:
		./download.sh

json: download
		./federation.py > federation.json
