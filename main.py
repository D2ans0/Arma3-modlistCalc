from sys import argv
try:
    import grequests
    async_fetch = True
except ImportError as err:
    print("Caught error {err}\nSkipping async")
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

def get_mod_size(html):
    try:
        parsed_response = bs(html.text, "html.parser").find("div", {"class":"detailsStatRight"})
        return parsed_response.text
    except Exception as e:
        print(f"Unable to get mod size due to {e}\nReturning 0.0 KB")
        return "0.0 KB"

def main(modlist_path):
    with open(modlist_path, "r") as raw_modlist:
        parsed_modlist = bs(raw_modlist, "html.parser")
        mod_count = 0
        modpack_size = 0
        mods = []
        for mod in parsed_modlist.find_all("tr"):
            name = mod.find("td", {"data-type":"DisplayName"}).text
            link = mod.find("a").get("href")
            size = get_mod_size(requests.get(link)) # scrape the steam workshop link to get mod size
            mods.append([name, link, size])
            modpack_size += size_to_bytes(size, return_unit="MB")
            mod_count += 1
            print(f"{size.ljust(12)}{name.ljust(60, '.')} {link}")

        print(f"\nTotal mod count:\t{mod_count}")
        print(f"Total modlist size:\t{round(modpack_size)} MB/{round(modpack_size/1000, 2)} GB")

def main_async(modlist_path):
    mod_count = 0
    modpack_size = 0
    mods = []
    reqs = []

    with open(modlist_path, "r") as raw_modlist:
        parsed_modlist = bs(raw_modlist, "html.parser")
        for mod in parsed_modlist.find_all("tr"):
            name = mod.find("td", {"data-type":"DisplayName"}).text
            link = mod.find("a").get("href")
            reqs.append(grequests.get(link))
            mods.append([name, link])
            mod_count += 1
            

    for response, mod in zip(grequests.imap(reqs, size=30), mods):
        mod.append(get_mod_size(response))
        modpack_size += size_to_bytes(mod[2], return_unit="MB")
        print(f"{mod[2].ljust(12)}{mod[0].ljust(60, '.')} {mod[1]}")

    print(f"\nTotal mod count:\t{mod_count}")
    print(f"Total modlist size:\t{round(modpack_size)} MB/{round(modpack_size/1000, 2)} GB")

if __name__ == "__main__":
    path = argv[-1]
    try:
        if (async_fetch == True and argv[1] != "force-sync") or argv[1] == "force-async":
            print("Fetching info asynchronously")
            main_async(path)
        else:
            import requests
            print("Fetching info normally")
            main(path)
    except IndexError as err:
        print(f"Caught error: {err}\n Switching to serial")
        main(path)
