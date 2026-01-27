import glob
import os


counter = 0

import requests
import hashlib

def scan_full_path(path_lst):
    global counter
    url = 'https://www.virustotal.com/api/v3/files'
    api_key = "dada308c922af9c795935496a42fc77430f24caf4e7376b65979323c35665c7d"
    headers_report = {"accept": "application/json","x-apikey": api_key}
    headers = {
        "accept": "application/json",
        "x-apikey": api_key}
    for file in path_lst:
        if os.path.isfile(file):
            print(f"is file:{file}")
            with open(file,'rb') as f:
                f = f.read()

            files = {"file":(file,f)}
            response = requests.post(url,headers=headers,files = files)
            try:
                print(response.json())
                file_report = get_hash_file(file)
                url_report = f"https://www.virustotal.com/api/v3/files/{file_report}"
                response_report = requests.get(url_report, headers=headers_report)

                if response.status_code == 200:
                    report_data = response_report.json()
                    stats = report_data["data"]["attributes"]["last_analysis_stats"]
                    counter += stats["malicious"]
                    print(response_report.text)
            except Exception:
                continue
        else:
            print(f"is folder:{file}")
            lst_file = to_list(file)
            scan_full_path(lst_file)
    return counter



def get_hash_file(file,algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()




def to_list(path):
    path_lst = glob.glob(f"{path}/*")
    return path_lst


def main():


    path = input("enter full path:")
    lst = to_list(path = path)
    scan_full_path(path_lst=lst)


if __name__ == "__main__":
    main()