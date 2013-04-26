#SYSTEM
import logging

def report_down(url, response):
    logging.error("*" * 100)
    logging.error("%s is down", url)
