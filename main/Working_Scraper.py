
import time
import writer
import selenium
import numpy as np
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

mod_lib = {
    "Touchscreen": "ts_pp",
    "Flashlight" : "fl_pp",
    "Half Time" : "ht_pp",
    "Easy" : "ez_pp",
    "Perfect!" : "pf_pp",
    "Sudden Death!" : "sd_pp",
    "No-mod" : "nm_pp",
    "Double Time" : "dt_pp",
    "Hidden" : "hd_pp",
    "No Choke" : "no_choke_pp",
    "Hard Rock" : "hr_pp"
}

def load(player_name,play_count,player = 1):
    e = Scraper(player_name,play_count,player)

class Scraper():
    def __init__(self,player_name,play_count,player) -> None:
        global driver
        driver = webdriver.Chrome('chromedriver')
        self.PLAYER_NAME,self.PLAY_COUNT = player_name,play_count
        self.shitsticks(player)

    def define_element(self,xpath:str):
        while True:
            try:
                obj = driver.find_element(by=By.XPATH, value=xpath)
                return obj
            except:
                time.sleep(1)

    def add_to_stats(self,xpath,num):
        global stats
        xpath = xpath[0:23] + str(num + 2) + xpath[23 + num + 2:]
        stats.append(self.define_element(xpath).get_attribute("innerHTML"))

    def shitsticks(self,player):
        global stats
        driver.get("https://osuchan.syrin.me/")

        search_bar = self.define_element("//*[@id=\"root\"]/div[2]/nav/div[3]/form/input")

        search_bar.clear()
        search_bar.send_keys(self.PLAYER_NAME)
        search_bar.send_keys(Keys.RETURN)

        show_more = self.define_element("//*[@id=\"root\"]/div[2]/main/div/div[7]/button")
        show_more.click()
        out = []


        for i in range(1,self.PLAY_COUNT + 1):
            driver.execute_script("arguments[0].click();", self.define_element(f"//*[@id=\"root\"]/div[2]/main/div/div[7]/div[{i}]"))

            stats = []
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/table/tbody/tr[1]/td[2]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/a").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/table/tbody/tr[2]/td[2]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/table/tbody/tr[3]/td[2]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/table/tbody/tr[4]/td[2]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/table/tbody/tr[5]/td[2]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[1]/span[5]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/table/tbody/tr[1]/td[2]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/table/tbody/tr[2]/td[2]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/table/tbody/tr[3]/td[2]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/span[2]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/span[3]").get_attribute("innerHTML"))
            #stats.append(define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/dv[2]/span[4]/span").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/span[5]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/table/tbody/tr[4]/td[2]").get_attribute("innerHTML"))
            stats.append(self.define_element(f"//*[@id=\"root\"]/div[{i + 2}]/div/div/div[2]/span[4]/span").get_attribute("innerHTML"))

            mods = []
            for ii in range(1,5):
                try:
                    mods.append(driver.find_element(by=By.XPATH, value=f"//*[@id=\"root\"]/div[{i + 1}]/div/div/div[1]/div/img[{ii}]").get_attribute("src"))
                except Exception as e:
                    break

            stats.append(mods)
            out.append(stats)
        
        for i in range(len(out)):
            out[i][-1] = "/".join([out[i][-1][ii][-6:-4] for ii in range(len(out[i][-1]))])
            out[i][-4] = "1" if out[i][-4] == "Choke" else "0"



        headdings = ["titles","bpms","lengths","css","ars","ods","stars","acc3s","acc2s","acc1s","accs","combos_full","combos","chokes","misses","pps","mods","hds","dts","hrs","ezs","hts","fls","nms"]
        titles = [out[i][1] for i in range(len(out))]
        bpms = [int(out[i][0]) for i in range(len(out))]
        lengths = [int(out[i][2][-2:]) + (int(out[i][2][:-3]) * 60) for i in range(len(out))]

        css = [float(out[i][3]) for i in range(len(out))]
        ars = [float(out[i][4]) for i in range(len(out))]
        ods = [float(out[i][5]) for i in range(len(out))]

        stars = [float(out[i][6]) for i in range(len(out))]
        acc3s = [int(out[i][7]) for i in range(len(out))]
        acc2s = [int(out[i][8]) for i in range(len(out))]

        acc1s = [int(out[i][9]) for i in range(len(out))]
        accs = [float(out[i][10]) for i in range(len(out))]
        chokes = [int(out[i][12]) for i in range(len(out))]

        misses = [int(out[i][13]) for i in range(len(out))]
        pps = [int(out[i][14].replace(",","")) for i in range(len(out))]
        combos_full = [out[i][11] for i in range(len(out))]
        combos = [int(combos_full[i][:combos_full[i].find("x")]) for i in range(len(out))]

        dts,hds,hrs,fls,ezs,hts,nms = [],[],[],[],[],[],[]
        mods = [out[i][-1] for i in range(len(out))]

        for i in mods:
            dts.append(1) if "NC" in i or "DT" in i else dts.append(0)
            hds.append(1) if "HD" in i else hds.append(0)
            hrs.append(1) if "HR" in i else hrs.append(0)
            fls.append(1) if "FL" in i else fls.append(0)
            ezs.append(1) if "EZ" in i else ezs.append(0)
            hts.append(1) if "HT" in i else hts.append(0)

            for ii in i:
                if ii != "":
                    nms.append(0)
                    break
            else:
                nms.append(1)

        mod_headdings = [mod_lib[self.define_element(f"/html/body/div/div[2]/main/div/div[8]/a[{i + 1}]/div/div[2]/span[1]").get_attribute("innerHTML").replace(",","")] for i in range(11)]
        mod_pps = [self.define_element(f"/html/body/div/div[2]/main/div/div[8]/a[{i + 1}]/div/div[3]/div[2]/span").get_attribute("innerHTML").replace(",","") for i in range(11)]

        lines = []                    
        data = {}

        for head in headdings:
            exec(f"self.ln = {head}")
            data[head] = self.ln

        for i in range(len(mod_headdings)):
            exec(f"self.ln = {mod_pps[i]}")
            data[mod_headdings[i]] = self.ln

        writer.write(data,f"P{player}")
        driver.close()

