from bs4 import BeautifulSoup
from urllib.request import urlopen

my_url = "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphic%20card"
uClient = urlopen(my_url)
page_soup = BeautifulSoup(uClient.read(), "html.parser")
uClient.close()

out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "Product_name,Rating,Current_price,Shipping_fee\n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

containers = page_soup.findAll("div", {"class":"item-container"})

for container in containers:
    product_title = container.a.img["title"]

    try:
        rating_container = container.findAll("a", {"class":"item-rating"})
        product_rating = rating_container[0].span.text
    except:
        product_rating = "N/A"
    
    try:
        shipping_price_container = container.findAll("li", {"class":"price-ship"})
        product_shipping_price = shipping_price_container[0].text.strip()
    except:
        product_shipping_price = "N/A"

    try:
        current_price_container = container.findAll("li", {"class":"price-current"})
        product_current_price = current_price_container[0].find("strong").text + current_price_container[0].find("sup").text 
    except:
        product_current_price = "N/A"

    f.write(product_title.replace(",", " | ") + "," + product_rating.replace("(", "").replace(")", "") + "," + "$" + product_current_price.replace(",", "") + "," + "$" + product_shipping_price.replace(",", "") + "\n")

f.close()

