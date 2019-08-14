import pandas as pd
import glob
import os


def get_all_parks():
    parks = set([])

    for file in glob.glob("data/visit_data/*.csv"):
        print(file)
        basename = os.path.basename(file)

        visiting_data = pd.read_csv(file, header=2)
        # set all park names to caps
        visiting_data["ParkName"] = visiting_data["ParkName"].apply(lambda x: x.upper())

        acreage_data = pd.read_excel(f"data/size_data/{basename[:-4]}.xlsx", header=1)
        acreage_data.rename(columns={"Area Name": "ParkName"}, inplace=True)
        acreage_data["ParkName"] = acreage_data["ParkName"].apply(lambda x: x.upper())

        acreage_data.set_index("ParkName", inplace=True)
        visiting_data.set_index("ParkName", inplace=True)

        merged = visiting_data.join(acreage_data)
        merged = merged.dropna()

        merged.reset_index(inplace=True)

        merged_parks = merged["ParkName"].tolist()

        for park in merged_parks:
            parks.add(park)

    return list(parks)
