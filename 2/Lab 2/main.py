import requests
import os
import zipfile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def main():
    try:
        os.mkdir("downloads")
    except OSError: pass

    for uri in download_uris:
        with requests.get(uri) as r:
            try:
                r.raise_for_status()
            except requests.HTTPError: continue
            path = uri.split('/')[-1]
            with open(path, 'wb') as f:
                f.write(r.content)
            with zipfile.ZipFile(path) as zip:
                zip.extractall("downloads")
            os.remove(path)
    pass


if __name__ == "__main__":
    main()
