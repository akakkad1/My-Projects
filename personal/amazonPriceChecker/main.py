import smtplib
import requests
import lxml
from bs4 import BeautifulSoup
import os
import dotenv

dotenv.load_dotenv()

product = input("What is the Amazon code of the product's price you want to check? ")
print("Searching...")

url = f"https://www.amazon.com/dp/{product}"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")

title = soup.find(id="productTitle").get_text().strip()
print(title)
check = input("Is this the correct product? Yes or No? ")

if check.upper() == "YES":
    price = soup.find(class_="a-offscreen").get_text()
    price_without_currency = price.split("$")[1]
    os.system('cls')
    price_as_float = float(price_without_currency)
    os.system('cls')
    print(f"The price of the {title} is: ${price_as_float}")
    BUY_PRICE = 400
    YOUR_EMAIL = os.getenv("EMAIL")
    YOUR_PASSWORD = os.getenv("PASSWORD")
    if price_as_float < BUY_PRICE:
        message = f"{title} is now {price}"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
          connection.starttls()
          result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
          connection.sendmail(
             from_addr=YOUR_EMAIL,
              to_addrs="aditkakkad@gmail.com",
              msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
          )

elif check.upper() == "NO":
   print("Please restart.")
   
else:
   print("Invalid input, please restart.")

