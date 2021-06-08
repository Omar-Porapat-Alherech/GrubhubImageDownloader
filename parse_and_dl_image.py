import requests
from requests.auth import HTTPBasicAuth
import re
from bs4 import BeautifulSoup
import os
from PIL import Image
import json


def parse_download(html, Section):
    print("=====================")
    print(Section)
    base_url = "https://restaurant.grubhub.com/"
    descriptions = []
    parent_dir = os.getcwd()
    if not os.path.exists(os.path.join(parent_dir, Section)):
        os.mkdir(Section)
    img_path = os.path.join(parent_dir, Section)
    with open(html, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        top_divs = soup.find_all("div", class_="sc-fzqBkg cifTAX sc-fzqPZZ dzaZp")
        for div in top_divs:
            # IMAGE
            try:
                img_class = div.find("div",
                                     class_="image-manager__background menu-item-media__background image-manager__background--has-border image-manager__background--has-round")
                img_url = re.findall('"([^"]*)"', img_class.attrs['style'])
            except AttributeError:
                pass
            # NAME
            item_name_class = div.find("h4")
            item_name = item_name_class.text
            # Description   
            item_description = div.find("p")
            # Download
            try:
                response = requests.get(img_url[0])
                full_img_path = img_path + "\\[" + Section + "]" + item_name.replace(" ", "_") + ".jpg"
                file = open(full_img_path, "wb")
                file.write(response.content)
                file.close()
            except UnboundLocalError:
                pass
            descriptions.append(str(item_name + " - " + item_description.text + "\n\n\n"))
        file = open(img_path + "\\" + Section + ".txt", "w")
        for item in descriptions:
            file.write(item)
        file.close()


def main():
    parse_download("Acai_Bowls.html", "Acai_Bowls")
    parse_download("Smoothie_Bowl.html", "Smoothie_Bowl")


if __name__ == "__main__":
    main()
