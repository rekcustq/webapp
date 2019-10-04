import os
import time
import schedule
import sqlite3
from sys import argv
from json import dump
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from multiprocessing import Pool

def get_meta(browser):
    metas = []
    for meta in browser.find_elements_by_tag_name('meta'):
        s = ''
        name = str(meta.get_attribute('name'))
        properties = str(meta.get_attribute('property'))
        content = str(meta.get_attribute('content').encode('ascii', 'ignore'))
        # print name, properties, content
        # if properties != 'None':
        #     s += '{0}: {1}'.format(properties, content)
        # elif name != '':
        #     s += '{0:15}: {1}'.format(name, content)
        s += content
        if s != '':
            metas.append(str(s))

    return '|'.join(metas)

def get_strings(browser, folder):
    preStrings = ['Hacked', 'hacker', 'haxor']
    getStrings = '|'.join(str(browser.find_element_by_tag_name('body').text.encode('utf-8')).split('\\n'))
    stat = False
    for txt in preStrings:
        if getStrings.find(txt) != -1:
            stat = True

    # save strings
    # f = open(folder + '\\strings.txt', 'w')
    # f.write(getStrings)
    # f.close()
    return stat, getStrings

def detect(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.get('https://' + url)
    (browser.page_source).encode('utf-8')

    folder = 'logs\\' + url.split('.')[0].split('/')[0]
    if not os.path.exists(folder):
        os.mkdir(folder)

    conn = sqlite3.connect('deface.db')
    c = conn.cursor()
    c.execute('''INSERT INTO urls (urlName)
                     SELECT "''' + url + '" WHERE NOT EXISTS (SELECT * FROM urls WHERE urlName = "' + url + '")')

    data = {}
    data[url] = []
    
    old_metas = c.execute('SELECT meta FROM urls WHERE urlName = "' + url + '";').fetchall()[0][0]
    new_metas = get_meta(browser)
    metaStat = False
    if not old_metas:
        c.execute('''UPDATE urls 
                     SET meta = "''' + new_metas + '''" 
                     WHERE urlName = "''' + url + '";')
    elif old_metas != new_metas:
        metaStat = True
    c.execute('''UPDATE urls 
                 SET metaStat = "''' + str(metaStat) + '''" 
                 WHERE urlName = "''' + url + '";')
    mts = ''
    if metaStat:
        mts = 'Changed'
    else:
        mts = 'Normal'

    strStat, strs = get_strings(browser, folder)
    c.execute('''UPDATE urls 
                 SET strStat = "''' + str(strStat) + '''" 
                 WHERE urlName = "''' + url + '";')
    sts = ''
    if strStat:
        sts = 'Illegal'
    else:
        sts = 'Normal.'

    data[url].append({ 
        'Meta': mts,
        'Strings': sts 
    })

    browser.close()
    conn.commit()
    conn.close()
    return data

def sched():
    conn = sqlite3.connect('deface.db')
    c = conn.cursor()
    urls = c.execute('SELECT urlName FROM urls').fetchall()
    conn.close()

    for url in urls:
        check(url[0])

def main():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if len(argv) > 1:
        url = argv[1]
    else:
        url = 'stackoverflow.com'

    r = open('logs.txt', 'w+')
    dump(detect(url), r, indent=4, sort_keys=True)
    r.write('\n')
    # p = Pool(processes=3)
    # p.map(check, urls)
    # p.close()

    print('Done.')

if __name__ == '__main__':
    schedule.every(5).minutes.do(main)
    main()

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)