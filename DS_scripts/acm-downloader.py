from os import getcwd
import time

from pyvirtualdisplay import Display
from selenium import webdriver

backoff = 10

class PaperDownloader(object):
    display = None
    browser = None

    def __init__(self):
        self.init_application()

    def init_application(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", getcwd()+"/articles")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        self.browser = webdriver.Firefox(firefox_profile=fp)

    def get_article(self,article):
        print('[ ] Downloading '+article, end=' ')
        #browser.get('https://dl.acm.org/citation.cfm?id={}'.format(num))
        self.browser.get(article)

        links = []
        # check the option
        for a in self.browser.find_elements_by_xpath("//a[@name='FullTextPDF']"):
            links.append(a.get_attribute('href'))

        self.browser.set_page_load_timeout(5)
        try:
            self.browser.get(links[0])
        except:
            pass

        print('}:)')

    def fini_application(self):
        self.browser.quit()
        self.display.stop()

if __name__=="__main__":
    application = PaperDownloader()

    with open('acm_links', 'r') as f:
        for article in f.read().split('\n'):
            try:
                application.get_article(article)
            except:
                print(':((')
                print('[-] Failure, restarting application')
                application.fini_application()
                application.init_application()
                print('[ ] Started application, sleeping for {} seconds'.format(backoff))
                time.sleep(backoff)
                try:
                    application.get_article(article)
                except:
                    print('[-] Fatal, banned :((')
                    application.fini_application()
                    sys.exit(1)

    application.fini_application()
