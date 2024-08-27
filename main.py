from sys import argv
import requests
from bs4 import BeautifulSoup as bs

def size_to_bytes(input_size, return_unit = "GB", append_unit = False):
    array = input_size.split()
    array[0] = float(array[0])
    if array[1] == "KB":
        bytes = array[0] * 1000
    elif array[1] == "MB":
        bytes = array[0] * (1000**2)
    elif array[1] == "GB":
        bytes = array[0] * (1000**3)
    elif array[1] == "KiB":
        bytes = array[0] * 1024
    elif array[1] == "MiB":
        bytes = array[0] * (1024**2)
    elif array[1] == "GiB":
        bytes = array[0] * (1024**3)

    if return_unit == "KB":
        out = bytes / 1000
    elif return_unit == "MB":
        out = bytes / (1000**2)
    elif return_unit == "GB":
        out = bytes / (1000**3)
    else:
        print("invalid return unit, defaulting to GB")
        out = bytes / (1000**3)

    if append_unit == True:
        out = str(out)+return_unit

    return out

def get_mod_size(mod_link):
    raw_response = requests.get(mod_link)
    parsed_response = bs(raw_response.content, "html.parser")
    return parsed_response.find("div", {"class":"detailsStatRight"}).text

def main(modlist_path):
    with open(modlist_path, "r") as raw_modlist:
        parsed_modlist = bs(raw_modlist, "html.parser")
        mod_count = 0
        modpack_size = 0
        for mod in parsed_modlist.find_all("tr"):
            name = mod.find("td", {"data-type":"DisplayName"}).text
            link = mod.find("a").get("href")
            size = get_mod_size(link)
            modpack_size += size_to_bytes(size, return_unit="MB")
            mod_count += 1
            print(f"{size.ljust(12)}{name.ljust(60, ".")} {link}")
        print(f"\nTotal mod count:\t{mod_count}")
        print(f"Total modlist size:\t{round(modpack_size)} MB/{round(modpack_size/1000, 2)} GB")

if __name__ == "__main__":
    path = argv[1]
    main(path)
