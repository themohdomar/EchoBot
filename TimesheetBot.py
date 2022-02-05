'''
    Web Scrawller to Fill in the hours worked upon
     weekly over the Firm's Timesheet portal for billing
     It is compatible to work with Multiple Project codes
     and custom hourly billing to be declared over a json
     input file.
'''

import json
from time import sleep
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Timesheetbot():

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(
            "https://pshr.quintiles.net/psp/h92prd/EMPLOYEE/HRMS/c/ROLE_EMPLOYEE.TL_MSS_EE_SRCH_PRD.GBL?"
            "FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_TIME_REPORTING.HC_RECORD_TIME.HC_"
            "TL_SS_JOB_SRCH_EE_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2CIsFolder&languageCd=ENG")
        # self.driver.maximize_window()
        print("Success")

    def load_data(self, file):
        try:
            with open(file) as f:
                data = json.load(f)
                print("Timesheet code JSON loaded")
                self.data = data
        except:
            print("Timesheet code JSON does not exist")
            exit(1)

    def multi_project_check(self, data):
        pro_count = int(data['Project count'])
        print("Projects :", pro_count)
        for i in range(pro_count):
            self.driver.find_element_by_xpath(
                "/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[10]/td[2]/div[1]/table"
                "/tbody/tr[2]/td/table/tbody/tr[2]/td[17]/div/a").click()
            sleep(2)
        print("Columns added")

    def holiday_checks(self):
        skip_r = 0
        skip_c = []
        for row in range(3):
            try:
                entry = self.driver.find_element_by_xpath(
                    "/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[10]/td[2]/div[1]/table"
                    "/tbody/tr[2]/td/table/tbody/tr[" + str(
                        row + 2) + "]/td[11]/div/span")
                if entry:
                    if entry.text == 'ADMN0000':
                        print("Skip row")
                        skip_r += 1
                        for col in range(3, 7):
                            if self.driver.find_element_by_xpath(
                                    "/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[10]/td[2]"
                                    "/div[1]/table/tbody/tr[2]/td/table/tbody/tr[" + str(
                                            row + 2) + "]/td[" + str(col) + "]/div/input").values == "8.50":
                                skip_c.append(col)
            except common.exceptions.NoSuchElementException:
                None

            skip_r += 2
            return skip_r, skip_c

    def enter_time(self, data, r, c):

        for row in range(int(data['Project count'])):
            for i in range(3, 16):
                if i == 8:
                    None
                elif i is 9:
                    self.driver.find_element_by_xpath(
                        "/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[10]/td[2]/div[1]"
                        "/table/tbody/tr[2]/td/table/tbody/tr[" + str(
                            row + r) + "]/td[9]/div/select/option[text()='" + data[str(row + 1)][
                            'Time Reporting Code'] + "']").click()
                else:
                    input_tab = self.driver.find_element_by_xpath(
                        "/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[10]"
                        "/td[2]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[" + str(
                            row + r) + "]/td[" + str(i) + "]/div/input")
                    # input_tab.clear()
                    if i is 10:
                        input_tab.send_keys(data[str(row + 1)]['Business Unit PC'])
                    elif i is 11:
                        input_tab.send_keys(data[str(row + 1)]['Project ID'])
                    elif i is 12:
                        input_tab.send_keys(data[str(row + 1)]['Activity ID'])
                    elif i is 13:
                        input_tab.send_keys(data[str(row + 1)]['Resourse Type'])
                    elif i is 14:
                        input_tab.send_keys(data[str(row + 1)]['Resource Category'])
                    elif i is 15:
                        input_tab.send_keys(data[str(row + 1)]['Resource Sub-Category'])
                    else:
                        if i not in c:
                            input_tab.send_keys(data[str(row + 1)]['Hours'])

        print("Ready to submit")

    def submit(self):

        self.driver.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr/td/div/table"
                                          "/tbody/tr[12]/td[2]/div/table/tbody/tr[2]/td/table"
                                          "/tbody/tr[2]/td[2]/div/a/span/input").click()
        print("Timesheet Submitted")
        sleep(3)

    def fill_time(self):
        self.load_data("Timesheetcode.json")
        self.driver.switch_to.default_content()
        frame = self.driver.find_element_by_name("TargetContent")
        # Switching to Inner Frame
        self.driver.switch_to.frame(frame)

        # Check for Multiple Projects
        if self.data["Multiple Projects"] == 'Y':
            self.multi_project_check(self.data)

        row, col = self.holiday_checks()
        sleep(10)
        self.enter_time(self.data, row, col)
        self.submit()
        self.driver.close()

