import smtplib
import threading
import time
import os

import requests
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render

from PriceTracker.models import UrlsToTrack

from dotenv import load_dotenv
load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept": "text/html, application/xhtml+xml, application/xml q = 0.9, image/webp, image/apng, */* q = 0.8"
}


def home(request):
    context = {}
    return render(request, "index.html", context)


def url_to_track(request):
    url = request.GET.get("url")
    print(url)

    urls_by_user = [
        url.url for url in UrlsToTrack.objects.filter(username=request.user)
    ]
    if urls_by_user.__contains__(request.GET.get("url")):
        context = scrap(url)
        context["message"] = "Already tracking this url"
        return render(request, "url_details.html", context)

    elif url.__contains__("https://www.amazon.in"):
        context = scrap(url)
        return render(request, "url_details.html", context)

    elif url.__contains__("https://www.amazon"):
        return render(request, "url_details.html", {"error": "Only amazon.in urls are supported for now"})

    else:
        return render(request, "url_details.html", {"error": "Not an Amazon Url"})


def scrap(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="title").getText().strip()
    price = soup.find("span", {"class": "a-price-whole"}).getText().strip()
    img = soup.find(id="landingImage")["src"].strip()
    price = price.replace(",", "").replace(".", "").replace("₹", "").strip()
    return {"title": title, "price": price, "img": img, "url": url}


def track(request):
    urls_by_user = [
        url.url for url in UrlsToTrack.objects.filter(username=request.user)
    ]
    context = {}
    if urls_by_user.__contains__(request.GET.get("url")):
        context["added_to_list"] = True
        return render(request, "index.html", context)
    else:
        url_save = UrlsToTrack()
        url_save.url = request.GET.get("url")
        url_save.username = request.user
        url_save.email = request.user.email
        url_save.exp_price = request.GET.get("price")
        url_save.save()
        context["added_to_list"] = True
        return render(request, "index.html", context)


def items(request):
    context = {"data": {}}

    i = 1
    for tracked_items in UrlsToTrack.objects.filter(username=request.user):
        price = scrap(tracked_items.url)["price"]
        context["data"]["item" + str(i)] = {"url": tracked_items.url, "exp_price": tracked_items.exp_price,
                                            "price": price}
        i += 1

    return render(request, "items.html", context)


def deleteItem(request):
    UrlsToTrack.objects.filter(username=request.user, url=request.GET.get("url")).delete()
    return redirect("/items/")


def mail(email, url, price):
    print(email, url, price)

    sender_email = os.getenv('SMTP_EMAIL')
    sender_email_password = os.getenv('SMTP_PASSWORD')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_email_password)
    message = "one of your product reached expected price."
    s.sendmail(sender_email, email, message)
    s.quit()


def track_items_in_db():
    time.sleep(36000)
    for url in UrlsToTrack.objects.all():
        if float(scrap(url.url)["price"]) <= float(url.exp_price):
            print(url.url)
            if not url.isEmailSent:
                mail(url.email, url.url, url.exp_price)
                url.isEmailSent = True
                url.save()

        else:
            print("nope")

    track_items_in_db()


thread = threading.Thread(target=track_items_in_db, args=(), kwargs={})
thread.setDaemon(True)
thread.start()
