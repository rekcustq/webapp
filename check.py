import os
import time
import schedule
import sqlite3
import concurrent.futures
import json
from sys import argv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from multiprocessing import Pool

def get_meta(browser):
    metas = []
    for meta in browser.find_elements_by_tag_name('meta'):
        s = ''
        name = str(meta.get_attribute('name'))
        properties = str(meta.get_attribute('property'))
        content = str(meta.get_attribute('content'))
        print(content)
        content.replace('"', '\'')
        # if properties != 'None':
        #     s += '{0}: {1}'.format(properties, content)
        # elif name != '':
        #     s += '{0:15}: {1}'.format(name, content)
        if properties != 'None' or name:
            s += content
        if s != '':
            metas.append(str(s))

    metas = '|'.join(metas)
    metas.replace("'|", '|')

    return metas.replace("'", "")

def get_strings(browser, folder):
    preStrings = ['Hacked', 'hacker', 'haxor']
    getStrings = '|'.join(str(browser.find_element_by_tag_name('body').text.encode('utf-8')).split('\\n'))
    stat = False
    for txt in preStrings:
        if getStrings.find(txt) != -1:
            stat = True

    return stat

def webStat(data, web):
    url = web[1]
    data[url] = []
    mts = 'Changed' if web[2] == 'True' else 'Normal' # metaStat
    sts = 'Illegal' if web[3] == 'True' else 'Normal' # strStat
    data[url].append({ 
        'meta': mts,
        'strings': sts 
    })

    return data

def detect(url):
    company = url[0]
    url = str(url[1])
    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.get('https://' + url)
    (browser.page_source).encode('utf-8')

    folder = 'logs\\' + company
    if not os.path.exists(folder):
        os.mkdir(folder)

    data = {}
    
    conn = sqlite3.connect('deface.db')
    c = conn.cursor()
    c.execute('''INSERT INTO urls (urlName, company)
                 SELECT "''' + url + '", "' + company + '''" 
                 WHERE NOT EXISTS 
                 (SELECT * FROM urls WHERE urlName = "''' + url + '")')

    old_metas = c.execute('SELECT meta FROM urls WHERE urlName = "' + url + '";').fetchall()[0][0]
    new_metas = get_meta(browser)
    metaStat = False
    # print(new_metas, '\n')
    if not old_metas:
        c.execute('''UPDATE urls 
                     SET meta = "''' + str(new_metas) + '''" 
                     WHERE urlName = "''' + url + '";')
    elif old_metas != new_metas:
        metaStat = True
    c.execute('''UPDATE urls 
                 SET metaStat = "''' + str(metaStat) + '''" 
                 WHERE urlName = "''' + url + '";')

    strStat = get_strings(browser, folder)
    c.execute('''UPDATE urls 
                 SET strStat = "''' + str(strStat) + '''" 
                 WHERE urlName = "''' + url + '";')

    web = c.execute('SELECT * FROM urls WHERE urlName = "' + url + '";').fetchall()[0]
    webStat(data, web)

    browser.close()
    conn.commit()
    conn.close()
    return data

def sched(company=''):
    conn = sqlite3.connect('deface.db')
    c = conn.cursor()
    if not company:
        urlNames = c.execute('SELECT urlName FROM urls WHERE company = "' + company + '"').fetchall()
    else:
        urlNames = c.execute('SELECT urlName FROM urls').fetchall()
    conn.close()
    urls = []
    for u in urlNames:
        if not company:
            company = u[0].split('.')[0]
        url = [company, u[0]]
        urls.append(url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(detect, urls)

    return 200

def main():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if len(argv) > 1:
        url = argv[1]
    else:
        url = 'stackoverflow.com'

    json.dumps(detect(url), indent=4, sort_keys=True)
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