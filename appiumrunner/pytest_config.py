import pytest
import os
from appium import webdriver
from py.xml import html
from ruamel.yaml import YAML

from appiumrunner.excel_reader import ExcelReader as reader

from appiumrunner.data_center import TestData

class ConfigPlugin:
    driver = None
    title = None
    username = None
    appium_url = None
    appium_run_info = {}


    def pytest_addoption(self,parser):
        parser.addoption(
            "--config", action="store", default="config.yaml", help="配置目录"
        )


    def pytest_configure(self,config):
        # 配置pytest
        # 删除Java_Home

        print("pytest配置中...",config._metadata)
        config._metadata.pop("JAVA_HOME")

        global title
        global username
        global appium_run_info
        global appium_url

        yaml = YAML(typ='safe')
        config_path = os.path.abspath(config.getoption("--config"))
        print("pytest配置中...",config_path)
        with open(config_path, encoding='utf-8') as file:
            data = yaml.load(file)
            config._metadata["Appium Runner"] = "https://github.com/crazyFeng/appium-runner"
            config._metadata["项目名称"] = data["projectname"]
            title = data["title"]
            username = data["username"]
            appium_url = data["appium_url"]
            appium_run_info = data["appium_run_info"]

            # 读取测试数据
            file_path = data["excel_file"]
            TestData.execute_infos.extend(reader.read_excel(file_path))
            TestData.ids.extend([
                "测试说明:{}".format(data["desc"]) for data in TestData.execute_infos
            ])


    def pytest_html_report_title(self,report):
        report.title = title


    @pytest.mark.optionalhook
    def pytest_html_results_summary(self,prefix):
        prefix.extend([html.p("测试人员信息: {}".format(username))])


    @pytest.fixture(scope="session")
    def driver(self):
        global driver
        driver = webdriver.Remote(appium_url, appium_run_info)
        yield driver



    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self,item):
        pytest_html = item.config.pluginmanager.getplugin('html')
        outcome = yield
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])
        if report.when == 'call':
            screen = driver.get_screenshot_as_base64()
            html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:360px;height:334px;" ' \
                   'align="right"/></div>' % screen
            extra.append(pytest_html.extras.html(html))
        report.extra = extra

    def pytest_runtest_protocol(self,item, nextitem):
       print("准备开始执行测试...",item)