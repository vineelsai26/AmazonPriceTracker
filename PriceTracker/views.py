import smtplib
import threading
import time

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from PriceTracker.models import UrlsToTrack

HEADERS = ({'User-Agent': 'Chrome'})


def home(request):
    context = {}
    # track_items_in_db()
    return render(request, "index.html", context)


def url_to_track(request):
    url = request.GET.get("url")
    print(url)

    urls_by_user = [url.url for url in UrlsToTrack.objects.filter(username=request.user)]
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
    title = soup.find(id="productTitle").getText().strip()
    price = soup.find(id="priceblock_ourprice").getText().strip()
    img = soup.find(id="landingImage")["src"].strip()
    price = price.lstrip("₹ ").strip().replace(",", "")
    return {"title": title, "price": price, "img": img, "url": url}


def track(request):
    urls_by_user = [url.url for url in UrlsToTrack.objects.filter(username=request.user)]
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


def mail(email, url, price):
    print(email, url, price)

    sender_email = ""
    sender_email_password = ""

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_email_password)
    message = "one of your product reached expected price."
    s.sendmail(sender_email, email, message)
    s.quit()


def track_items_in_db():
    for url in UrlsToTrack.objects.all():
        if float(scrap(url.url)["price"]) <= float(url.exp_price):
            print(url.url)
            if not url.isEmailSent:
                mail(url.email, url.url, url.exp_price)
                url.isEmailSent = True
                url.save()

        else:
            print("nope")

    time.sleep(36000)
    track_items_in_db()


t = threading.Thread(target=track_items_in_db, args=(), kwargs={})
t.setDaemon(True)
t.start()
