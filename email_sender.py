import requests
import keys
import smtplib
import os
import ssl

email = os.getenv("GMAIL")
password = os.getenv("GMAIL_PASS")
host = "smtp.gmail.com"
port = 465
context = ssl.create_default_context()

topic = "bitcoin"
url = f"https://newsapi.org/v2/everything?" \
      f"q={topic}&" \
      f"language=en&" \
      f"from=2023-08-15&" \
      f"sortBy=relevancy&" \
      f"apiKey={keys.news_api_key}"

response = requests.get(url)
content = response.json()
message = f"Subject: Today's news about {topic.capitalize()} \n"

for article in content['articles'][:20]:
    if article['source']['id']:
        title = article['title']
        description = article['description']
        news_link = article['url']
        if title and description:
            message += title + "\n" + description + "\n" + news_link + "\n"*2

print(message)
message = message.encode("utf-8")


if __name__ == "__main__":
    pass

    # with smtplib.SMTP_SSL(host, port, context=context) as server:
    #     server.login(email, password)
    #     server.sendmail(from_addr=email, to_addrs="halilhasmer@gmail.com", msg=message)
