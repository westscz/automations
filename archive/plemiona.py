from webbot import Browser
import os

world = "130"
village = 53163
login = ""
password = ""


web = Browser()  # showWindow=False)
web.go_to("https://www.plemiona.pl/")
web.type(login, into="Email")
web.click("NEXT", tag="span")
web.type(password, into="Password", id="passwordFieldId")  # specific selection
web.click("Logowanie")
web.click("NEXT", tag="span")
web.click("Świat 130")
web.click("Ratusz")

web.go_to("https://pl{}.plemiona.pl/game.php?village={}&screen=main".format(world, village))

source = web.get_page_source()
from lxml import html

tree = html.fromstring(source)
x = tree.xpath('//table[@id="buildings"]//tr')
x = x[1].getchildren()
print(dir(x[1]))
info, w, s, i, _, _, b = x
print("wood", w.attrib["data-cost"])
print("stone", s.attrib["data-cost"])
print("iron", i.attrib["data-cost"])
print(b.getchildren())
