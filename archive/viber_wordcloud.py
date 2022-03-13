"""
Get all messages for given number from csv file (viber csv format) and create WordCloud
"""

import csv
import pandas
from wordcloud import WordCloud


def func_pandas_join(file):
    def parse_my_file(filename):
        with open(filename) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            last_row = None
            for row in spamreader:
                if (row[3][0] if len(row) > 3 else None) == "+":
                    msg = ",".join(row[4:])
                    if not msg:
                        msg = "Null"
                    last_row = row[:4] + [msg.lower()]
                else:
                    row = row if len(row) > 0 else ["Null"]
                    msg = ",".join(row)
                    last_row = last_row[:4] + [msg.lower()]
                yield last_row

    my_parser = parse_my_file(file)
    return pandas.DataFrame(
        my_parser, columns=["date", "hour", "person", "number", "message"]
    )


def get_words_count(words_list):
    s = words_list.str.split("[ .]+", expand=True).stack().value_counts()
    print(s)
    return s


if __name__ == "__main__":
    x = func_pandas_join("in.csv")
    y = x.query('number=="+48xxxxxxxxx"')["message"]
    w = get_words_count(y)  # x['message'])
    w.reset_index().to_csv("out.csv")

    wc = WordCloud(background_color="white", max_words=2000)
    wc.generate_from_frequencies(w.to_dict())
    wc.to_file("alice.png")
