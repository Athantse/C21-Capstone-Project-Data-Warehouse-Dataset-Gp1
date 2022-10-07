# -*- coding: utf-8 -*-
from selenium.webdriver import Chrome
import time
import pandas as pd

def spiderList():
    dataList = [
                ['17', '酒精飲料', "tosubmit(17,'酒精飲料', 'Alcoholic beverages')"],
                ['13', '除魚類外的水產動物', "tosubmit(13,'除魚類外的水產動物','Aquatic animals other than fish')"],
                ['01', '穀類及其製品', "tosubmit(01,'穀類及其製品','Cereals and cereal products')"],
                ['09', '蛋類及其製品', "tosubmit('09','蛋類及其製品','Eggs and egg products  ')"],
                ['15', '油脂類', "tosubmit('15','油脂類','Fats and oils')"],
                ['12', '魚類及其製品', "tosubmit('12','魚類及其製品','Fish and fish products')"],
                ['11', '冰凍甜點', "tosubmit('11','冰凍甜點','Frozen confections')"],
                ['04', '水果類及其製品', "tosubmit('04','水果類及其製品','Fruits and fruit products')"],
                ['08', '野味類及其製品', "tosubmit('08','野味類及其製品','Games and game products')"],
                ['02', '豆類及其製品', "tosubmit('02','豆類及其製品','Legumes and legume products')"],
                ['06', '畜肉類及其製品', "tosubmit('06','畜肉類及其製品','Meat and meat products')"],
                ['10', '奶類及其製品', "tosubmit('10','奶類及其製品','Milk and milk products')"],
                ['16', '不含酒精飲料', "tosubmit('16','不含酒精飲料','Non-alcoholic beverages')"],
                ['05', '堅果與種子及其製品', "tosubmit('05','堅果與種子及其製品','Nuts, seeds and their products')"],
                ['07', '禽肉類及其製品', "tosubmit('07','禽肉類及其製品','Poultry and poultry products')",
                ['03', '蔬菜類及其製品', "tosubmit('03','蔬菜類及其製品','Vegetables and vegetable products')"],
                ['40', '即食食物', "tosubmit('40','即食食物','Ready-to-eat foods')"],
                ['22', '沙律(色拉)', "tosubmit('22','沙律(色拉)','Salads')"],
                ['26', '小食', "tosubmit('26','小食 ','Snacks')"],
                ['21', '湯類', "tosubmit('21','湯類','Soups')"],
                ['18', '糖及糖類製品', "tosubmit('18','糖及糖類製品 ','Sugars and sweets ')"]
                ]
               ]
    for data in dataList:
        detailList = []
        id = data[0]
        title = data[1]
        js = data[2]
        web = Chrome()
        web.get('https://www.cfs.gov.hk/tc_chi/nutrient/search1.php')
        time.sleep(3)
        web.execute_script(js)
        time.sleep(2)
        web.execute_script(f"tosubmit('{id}','-1')")
        time.sleep(2)
        all_pages = web.window_handles

        web.switch_to.window(all_pages[-1])

        contents = web.find_elements_by_xpath('/html/body/div[2]/form/div[2]/table/tbody//tr')
        num = 2
        for c in contents:
            try:
                # 食物名稱
                foodName = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[1]'.format(num)).text
                # 能量
                energy = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[5]'.format(num)).text
                # 蛋白質
                protein = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[6]'.format(num)).text
                # 碳水化合物
                carbo = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[7]'.format(num)).text
                # 脂肪
                fat = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[8]'.format(num)).text
                # 膳食纖維
                fiber = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[9]'.format(num)).text
                # 糖
                sugar = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[10]'.format(num)).text
                # 鈉
                sodium = c.find_element_by_xpath(
                    '/html/body/div[2]/form/div[2]/table/tbody/tr[{}]/td[14]'.format(num)).text
                message = foodName, title, energy, protein, carbo, fat, fiber, sugar, sodium
                print(message)
                detailList.append(list(message))
                num += 1
            except:
                num += 1
                pass
        columns = ['食物名稱', '種類', '能量', '蛋白質', '碳水化合物', '脂肪', '膳食纖維', '糖', '鈉']
        dataF = pd.DataFrame(detailList, columns=columns)
        print(dataF)
        dataF.to_excel(f"{title}.xlsx")
        time.sleep(1)
        web.close()


if __name__ == '__main__':
    spiderList()
