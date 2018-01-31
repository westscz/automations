"""
Get data from Otodom.pl
"""

class UrlCreator:
    delimiter="&"
    search = "search%5B"
    url = "https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?"

    def price_from(self, price):
        self._add_to_url("filter_float_price%3Afrom%5D={}".format(price))

    def price_to(self, price):
        self._add_to_url("filter_float_price%3Ato%5D={}".format(price))

    def price_per_m_from(self, price):
        self._add_to_url("filter_float_price_per_m%3Afrom%5D={}".format(price))

    def price_per_m_to(self, price):
        self._add_to_url("filter_float_price_per_m%3Ato%5D=={}".format(price))

    def measure_from(self, m3):
        self._add_to_url("filter_float_m%3Afrom%5D={}".format(m3))

    def measure_to(self, m3):
        self._add_to_url("filter_float_m%3Ato%5D={}".format(m3))

    def rooms_num(self, num):
        for i, room in enumerate(num):
            self._add_room(i, room)

    def _add_room(self, enum, rooms):
        self._add_to_url("filter_enum_rooms_num%5D%5B{}%5D={}".format(enum, rooms))

    def _add_to_url(self, parameter):
        self.url = self.url + self.search + parameter + self.delimiter

    def print_url(self):
        print(self.url)
        return self.url

x = UrlCreator()
x.rooms_num([1,2,4])
x.measure_from("50")
x.measure_to("70")

x.price_from("200000")
x.price_to("250000")
y = x.print_url()

import requests
x = requests.get(y)
# print(x.text)
from lxml import html
import xml.etree.ElementTree as ET
tree = html.fromstring(x.text)
l = tree.xpath("//div[@class='offer-item-details']//li [@class='offer-item-price']")
print(l[0].text)
print(len(l))

# <div class="offer-item-details">
#                 <header class="offer-item-header">
#             <h3>
#                 <a href="https://www.otodom.pl/oferta/mieszkanie-2-pokojowe-m-15-38-54-m2-ID3iu8Q.html#01f48d3526" data-tracking="click_body" data-tracking-data="{&quot;touch_point_button&quot;:&quot;title&quot;}" data-featured-tracking="listing_no_promo">
#                     <strong class="visible-xs-block">38,54 m²</strong>
#                     <span class="text-nowrap">
#                         <span class="offer-item-title">mieszkanie 2 pokojowe M-15 -38,54 m2</span>
#                     </span>
#                 </a>
#             </h3>
#             <p class="text-nowrap hidden-xs">Mieszkanie na sprzedaż: Wrocław</p>
#         </header>
#         <ul class="params" data-tracking="click_body" data-tracking-data="{&quot;touch_point_button&quot;:&quot;body&quot;}">
#               <li class="offer-item-rooms hidden-xs">2 pokoje</li>
#               <li class="offer-item-price">#                                                     180 000 zł                                                                                            </li>
#               <li class="hidden-xs offer-item-area">38,54 m²</li>
#               <li class="hidden-xs offer-item-price-per-m">4 670 zł/m²</li>
#                                                                                                                                                                 </ul>
#     </div>