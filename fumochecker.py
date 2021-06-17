#written by abbez@borkgang
#3AM project, written in 1 hour

import time
import requests
from socket import timeout
import errno
import json

patchouli_fumo = "パチュリー・ノーレッジ+ふもふも+ぬいぐるみ+東方"
reimu_red_fumo = "博麗 霊夢 ぬいぐるみ+ふもふも"
cirno_fumo = "チルノ+ふもふも"
remilia_scarlet_fumo = "レミリア・スカーレット+ふもふも"
flandre_fumo = "フランドール・スカーレット+ふもふも"
marisa_fumo = "霧雨魔理沙+ふもふも"
yukari_fumo = "八雲紫+ふもふも"
alice_fumo = "アリス・マーガトロイド+ふもふも"

already_posted_fumos = []

def not_in_list(link):
    f = open("fumolist.txt", "r")
    if link in f.read():
        return False
    else:
        return True

def post_to_webhook(message, price, link):
    try:
        if not_in_list(link):
            f = open("fumolist.txt", "a")
            f.write(link + " | ")
            f.close()
            
            cheap_message = "Spotted Fumo!"
            if int(price) < 6000:
                cheap_message = "Spotted VERY Cheap Fumo!"
            elif int(price) < 10000:
                cheap_message = "Spotted Cheap Fumo!"
            elif int(price) < 15000:
                cheap_message = "Spotted Semi-Cheap Fumo!"
            elif int(price) < 20000:
                cheap_message = "Spotted Semi-Expensive Fumo!"
            
            data = {
                "username": "Fumo Price Checker"
            }
            data["embeds"] = [
                {
                    "description": message + " has been spotted!\nPrice: " + price + " Yen\nLink: " + link + "\n\nNOTE: These may not be plushies and instead other items for them.\nNOTE 2: Make sure these are not fakes!",
                    "title": cheap_message
                }
            ]
            requests.post("https://discord.com/api/webhooks/DISCORD WEBHOOK HERE", json = data)
            return True
        else:
            return False
    except:
        return False

def check_yahoo_auction(fumo, fumo_name):
    req = requests.get("https://auctions.yahoo.co.jp/search/search?p={}".format(fumo))
    if req.text.find("</span><span class=\"Product__priceValue u-textRed\">") != -1:
        text = req.text
        for i in range(50):
            try:
                if i != 0:
                    auction = text.split("u-textRed\">")[i].split("円")[0].replace(",", "")
                    link = text.split("<h3 class=\"Product__title\"><a class=\"Product__titleLink js-rapid-override\" data-auction-id=\"")[i].split("href=")[1].split("\" t")[0].replace("\"", "")
                    if int(auction) < 20000:
                        time.sleep(2)
                        link_req = requests.get(link)
                        link_title = link_req.text.split("<h1 class=\"ProductTitle__text\">")[1].split("</h1>")[0]
                        if link_title.find("典缶バッジ付") != -1: #with badge
                            if post_to_webhook(fumo_name, auction, link):
                                print("[BORKGANG.COM FUMO CHECKER] - Posted " + fumo_name + " to webhook")
                            else:
                                print("[BORKGANG.COM FUMO CHECKER] - Unable to post to webhook")
                        else:
                            if link_title.find("バッジ") == -1: #no badge in title, prevents just badge ones
                                if post_to_webhook(fumo_name, auction, link):
                                    print("[BORKGANG.COM FUMO CHECKER] - Posted " + fumo_name + " to webhook")
                                else:
                                    print("[BORKGANG.COM FUMO CHECKER] - Unable to post to webhook")
            except:
                pass
        return True
    else:
        return False

while True:
    try:
        check_yahoo_auction(patchouli_fumo, "Patchouli Knowledge Fumofumo")
        time.sleep(1)
        check_yahoo_auction(reimu_red_fumo, "Red Reimu Fumofumo")
        time.sleep(1)
        check_yahoo_auction(cirno_fumo, "Cirno Fumofumo")
        time.sleep(1)
        check_yahoo_auction(remilia_scarlet_fumo, "Remilia Scarlet Fumofumo")
        time.sleep(1)
        check_yahoo_auction(flandre_fumo, "Flandre Scarlet Fumofumo")
        time.sleep(1)
        check_yahoo_auction(marisa_fumo, "Marisa Kirisame Fumofumo")
        time.sleep(1)
        check_yahoo_auction(yukari_fumo, "Yukari Yakumo Fumofumo")
        time.sleep(1)
        check_yahoo_auction(alice_fumo, "Alice Margatroid Fumofumo")
        time.sleep(5)
    except:
        print("[BORKGANG.COM FUMO CHECKER] - Unexpected exception")
        time.sleep(10)
        pass
    time.sleep(380)