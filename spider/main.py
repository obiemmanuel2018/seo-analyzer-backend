from .Audit import *
import threading
from queue import Queue
from .CrawlerBot.main import create_workers
from .CrawlerBot.main import crawl
from .CrawlerBot.main import setup
from .CrawlerBot.main import *
from .CrawlerBot.domain import *
from .CrawlerBot.general import *
from .CrawlerBot.linkfinder import *
from .CrawlerBot import spider
from .general2 import *
from .Scrap_Webpage import scrape
from multiprocessing import Pool
import time
from django.conf import settings
import os
import json


# def load_and_write_workbook(workbook_name, name_of_audit_sheet, result):
#     Newbook = load_workbook(workbook_name + ".xlsx")
#     Newbook.create_sheet(name_of_audit_sheet)
#     worksheet = Newbook[name_of_audit_sheet]
#     if any(isinstance(el, list) for el in result):
#         result_in = [item for sublist in result for item in sublist]
#     else:
#         result_in = result
#     m = len(result_in)
#     for i in range(1, m + 1):
#         worksheet.cell(row=i, column=1, value=(result_in[i - 1]))
#     Newbook.save(filename=PROJECT_NAME + '.xlsx')



def analyzer(PROJECT_NAME, HOMEPAGE):
    setup(PROJECT_NAME=PROJECT_NAME, HOMEPAGE=HOMEPAGE)
    create_workers()
    crawl()

    time.sleep(6)
    # print("Auditing")

    scrapped_data = get_scrapped_data(os.path.join(settings.PROJECT_ROOT,PROJECT_NAME,'crawled.txt'))
    duplicate_titles = scrapped_data.duplicate_titles()
    duplicate_descriptions = scrapped_data.duplicate_meta_descriptions()
    missing_descriptions = scrapped_data.get_missing_descriptions()
    missing_titles = scrapped_data.get_missing_titles()
    missing_h1 = scrapped_data.get_missing_h1()
    duplicate_h1 = scrapped_data.get_duplicate_h1()
    missing_canonicals = scrapped_data.get_missing_canonicals()
    wrong_canonicals = scrapped_data.improper_canonicals()
    missing_viewports = scrapped_data.missing_viewports()
    low_titles = scrapped_data.get_titles_with_less_content()
    low_meta = scrapped_data.get_meta_des_with_less_content()


    return {
        'duplicate_titles': duplicate_titles,
        'duplicate_descriptions': duplicate_descriptions,
        'missing_descriptions': missing_descriptions,
        'missing_titles' :  missing_titles,
        'missing_h1': missing_h1,
        'duplicate_h1':duplicate_h1,
        'missing_canonicals': missing_canonicals,
        'wrong_canonicals': wrong_canonicals,
        'missing_viewports': missing_viewports,
        'low_titles':low_titles,
        'low_metas':low_meta
    }






