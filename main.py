import datetime as dt
import smtplib
import ssl
import pandas as pd
import requests
import keys


class ExcelFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_data(self):
        df = pd.read_excel(self.filepath)
        return df


class Email:
    email = "halilpython@gmail.com"
    password = "<your-password-here>"

    def __init__(self, address, subject, content):
        self.address = address
        self.subject = f"Subject:{subject} \n"
        self.content = content

    def send(self):
        """I'm not really sending here bc I don't want my inbox to fill with these."""
        host = "smtp.gmail.com"
        port = 465
        context = ssl.create_default_context()
        msg = self.subject + self.content
        msg_encoded = msg.encode("utf-8")
        # with smtplib.SMTP_SSL(host, port, context=context) as server:
        #     server.login(self.email, self.password)
        #     server.sendmail(from_addr=self.email, to_addrs=self.address, msg=msg_encoded)
        return msg


class NewsFeed:
    def __init__(self, topic):
        self.topic = topic

    def get(self, prior_days=15):
        from_date = (dt.datetime.now() - dt.timedelta(days=prior_days)).strftime("%Y-%m-%d")
        url = f"https://newsapi.org/v2/everything?" \
              f"q={self.topic}&" \
              f"language=en&" \
              f"from={from_date}&" \
              f"sortBy=relevancy&" \
              f"apiKey={keys.news_api_key}"
        response = requests.get(url)
        content = response.json()
        result = ""
        for article in content['articles'][:20]:
            if article['source']['id']:
                title = article['title']
                description = article['description']
                news_link = article['url']
                if title and description:
                    result += title + "\n" + description + "\n" + news_link + "\n"*2
        return result


class User:
    def __init__(self, name, surname, email, interest):
        self.full_name = name + " " + surname
        self.email = email
        self.interest = interest

    def prepare_subject(self):
        today = dt.datetime.now().strftime("%A")
        topic = self.interest
        subject = f"Hello {self.full_name}... Your {topic} news for {today}"
        return subject


if __name__ == "__main__":
    excel = ExcelFile("people.xlsx")
    df = excel.get_data()
    for _, value in df.iterrows():
        user = User(value["name"], value["surname"], value["email"], value["interest"])
        subject = user.prepare_subject()

        news = NewsFeed(user.interest)
        news_feed = news.get(prior_days=7)

        email = Email(user.email, subject, news_feed)
        print(email.send())
