import csv

def load_iocs(file_path):
    iocs = {"ip": set(), "domain": set(), "hash": set()}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            iocs[row["type"]].add(row["value"])
    return iocs

def match_iocs(log_path, iocs):
    matches = []
    with open(log_path, 'r') as f:
        for line in f:
            for ip in iocs["ip"]:
                if ip in line:
                    matches.append(f"⚠️ Matched IP: {ip}")
            for domain in iocs["domain"]:
                if domain in line:
                    matches.append(f"⚠️ Matched Domain: {domain}")
            for hash in iocs["hash"]:
                if hash in line:
                    matches.append(f"⚠️ Matched Hash: {hash}")
    return matches

if __name__ == "__main__":
    iocs = load_iocs("data/indicators.csv")
    results = match_iocs("logs/sample.log", iocs)
    for match in results:
        print(match)
