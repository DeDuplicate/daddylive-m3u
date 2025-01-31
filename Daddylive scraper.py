from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import json

import tvlogo
import fetcher

daddyLiveChannelsFileName = '247channels.html'
daddyLiveChannelsURL = 'https://thedaddy.to/24-7-channels.php'

tvLogosFilename = 'tvlogos.html'
tvLogosURL = 'https://github.com/tv-logo/tv-logos/tree/main/countries/united-states'

matches = []

def search_streams(file_path, keyword):
    """
    Searches for a keyword in a file and outputs the stream number and name for each match.

    Parameters:
    file_path (str): The path to the file.
    keyword (str): The keyword to search for.

    Returns:
    list: A list of tuples containing the stream number and name for each match.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                if keyword.lower() in link.text.lower():
                    href = link['href']
                    stream_number = href.split('-')[-1].replace('.php', '')
                    stream_name = link.text.strip()
                    match = (stream_number, stream_name)

                    if match not in matches:
                        matches.append(match)

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")

    return matches

def search_channel_ids(file_path, search_string, idMatches):
    """
    Parses an XML file and finds channel tags with an id attribute that matches the search string.

    Parameters:
    file_path (str): The path to the XML file.
    search_string (str): The string to search for within the id attribute.
    idMatches (list): A list to store matches.

    Returns:
    list: A list of dictionaries {'id': ..., 'source': ...} that match the search string.
    """
    search_words = search_string.lower().split()  # Split the search string into words

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for channel in root.findall('.//channel'):
            channel_id = channel.get('id')
            if channel_id:
                for word in search_words:
                    if word in channel_id.lower():
                        if channel_id not in [c['id'] for c in idMatches]:
                            idMatches.append({'id': channel_id, 'source': file_path})
                            if 'National Geographic' in channel_id:
                                print("What")
                        # Break if at least one word matches (prevents duplicates)
                        break

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except ET.ParseError:
        print(f"The file {file_path} is not a valid XML file.")

    return idMatches

def print_possible_ids(possibleIds, channel):
    """
    Prints the possible IDs with their indices and takes user input to make a selection.

    Parameters:
    possibleIds (list): The list of possible IDs to print.
    channel (str): The channel name for which we are selecting.

    Returns:
    dict or int: The selected dictionary (with 'id'/'source') or -1 if none is selected.
    """
    if possibleIds:
        print("0). I dont want this channel.")
        for index, match in enumerate(possibleIds):
            # Use double quotes around the f-string
            print(f"{index+1}). {match['id']} {match['source']}")

        while True:
            try:
                user_input = int(input(f"Select the index of the Channel ID you want ({channel}): ")) - 1
                if user_input == -1:
                    print("Not adding a match for this channel.")
                    return -1
                if 0 <= user_input < len(possibleIds):
                    selected_id = possibleIds[user_input]
                    print(f"You selected: {selected_id}")
                    return selected_id
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print("No matches found.")

def delete_file_if_exists(file_path):
    """
    Checks if a file exists and deletes it if it does.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    bool: True if the file was deleted, False if it didn't exist.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"File {file_path} deleted.")
        return True
    else:
        print(f"File {file_path} does not exist.")
        return False

# Delete old files if they exist
delete_file_if_exists('out.m3u8')
delete_file_if_exists('tvg-ids.txt')

# Define EPG XML files to fetch
epgs = [
    {'filename': 'epgShare1.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz'},
    {'filename': 'epgShare2.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS2.xml.gz'},
    {'filename': 'epgShare3.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz'},
    {'filename': 'epgShare4.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_UK1.xml.gz'},
    {'filename': 'epgShare5.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_AU1.xml.gz'},
    {'filename': 'epgShare6.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_IE1.xml.gz'},
    {'filename': 'epgShare7.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz'},
    {'filename': 'epgShare8.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_ZA1.xml.gz'},
    {'filename': 'epgShare8.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz'},
    {'filename': 'bevyCustom.xml', 'url': 'https://www.bevy.be/generate/8TbvgWSctM.xml.gz'}
]

# Fetch HTML pages
fetcher.fetchHTML(daddyLiveChannelsFileName, daddyLiveChannelsURL)
fetcher.fetchHTML(tvLogosFilename, tvLogosURL)

# Fetch EPG files
for epg in epgs:
    fetcher.fetchXML(epg['filename'], epg['url'])

# Define search terms
search_terms = [
    # "Disney",
    # "Altitude",
    # "ABC",
    # "NBC",
    # "TNT",
    # "Lifetime",
    # "CBS",
    # "Discovery",
    # "NHL",
    # "gamecenter",
    # "Fox",
    # "wnyw",
    # "FOX USA",
    # "HBO",
    # "ESPN",
    # "A&E",
    # "AMC",
    # "FX",
    # "NBA",
    # "NFL",
    # "Network",
    # "TMC",
    # "Showtime",
    # "Animal Planet",
    # "pbs",
    # "BBC America",
    # "Nick",
    # "Starz",
    # "syfy",
    # "Bally",
    # "NHL",
    # "ESPN",
    # "cinemax",
    # "fox",
    "nfl network"
]

# Extract payload from the TV logos HTML
payload = tvlogo.extract_payload_from_file(tvLogosFilename)
print(json.dumps(payload, indent=2))

# Search the local HTML (247channels.html) for matches
for term in search_terms:
    search_streams(daddyLiveChannelsFileName, term)

# For each matched channel in 'matches', gather EPG IDs and TV logos
for channel in matches:
    # Normalize the channel name for searching in EPG IDs/logos
    word = (
        channel[1]
        .lower()
        .replace('channel', '')
        .replace('hdtv', '')
        .replace('tv', '')
        .replace(' hd', '')
        .replace('2', '')
        .replace('sports', '')
        .replace('1', '')
        .replace('usa', '')
    )

    possibleIds = []

    user_input = int(input(f"Do you want this channel? 0 = no 1 = yes ({channel[1]}): "))

    if user_input == 0:
        continue
    else:
        print("Searching for matches...")

    # Search for EPG IDs among the fetched epg files
    for epg in epgs:
        search_channel_ids(epg['filename'], word, possibleIds)

    # Search for matching logos
    logo_matches = tvlogo.search_tree_items(word, payload)

    # Let the user pick the correct EPG ID
    channelID = print_possible_ids(possibleIds, channel[1])

    if channelID != -1 and channelID is not None:
        # Let the user pick a logo (if any matches)
        tvicon = print_possible_ids(logo_matches, channel[1])
        if tvicon == -1 or tvicon is None:
            tvicon = {'id': {'path': ''}}

        # Write the final M3U entry
        initialPath = payload.get('initial_path', '')
        with open("out.m3u8", 'a', encoding='utf-8') as file:
            file.write(
                f"#EXTINF:-1 tvg-id=\"{channelID['id']}\" tvg-name=\"{channel[1]}\" "
                f"tvg-logo=\"https://raw.githubusercontent.com{initialPath}{tvicon['id']['path']}\" "
                f"group-title=\"USA (DADDY LIVE)\", {channel[1]}\n"
            )
            file.write(f"https://xyzdddd.mizhls.ru/lb/premium{channel[0]}/index.m3u8\n\n")

        # Write the final ID to tvg-ids.txt
        with open("tvg-ids.txt", 'a', encoding='utf-8') as file:
            file.write(f"{channelID['id']}\n")

print("Number of Streams: ", len(matches))
