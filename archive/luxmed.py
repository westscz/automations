"""
Log to luxmed and check if there is chance to change visit hour/date
"""
import os

import webbot


def wait_for_and_click(browser, text):
    while not browser.exists(text=text):
        pass
    browser.click(text=text)


LUXMED_LOGIN = os.environ.get("LUXMED_LOGIN", "")
LUXMED_PASS = os.environ.get("LUXMED_PASS", "")

w = webbot.Browser(showWindow=True)
w.go_to("https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogOn")
w.type(LUXMED_LOGIN, id="Login")
w.type(LUXMED_PASS, id="TempPassword")
w.type(LUXMED_PASS, id="Password")
w.click(tag="div", classname="submit")

wait_for_and_click(
    w,
    text="""
            Chcę umówić wizytę lub badanie
        """,
)
wait_for_and_click(w, text="Wizyta w placówce")
wait_for_and_click(w, text="Wybierz usługę")
wait_for_and_click(
    w,
    text="""
                        Konsultacja psychiatry - wizyta pierwszorazowa
                    """,
)
wait_for_and_click(
    w,
    text="""
                        Konsultacja psychologa - wizyta pierwszorazowa
                    """,
)
wait_for_and_click(
    w,
    text="""
                    Cały dzień
                    """,
)
w.click(tag="input", id="reservationSearchSubmitButton")
# while not w.find_elements(xpath=".//div/text", tag="text"):
#     pass
# available = w.find_elements(xpath=".//div/text", tag="text").pop(0).text
# print(available)

# w.click(text="Wyloguj się")
# w.go_to("https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogOut")
# w.close_current_tab()
