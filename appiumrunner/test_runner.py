import pytest
from appiumrunner.executor import execute
from appiumrunner.data_center import TestData


class TestMain():

    # pytest 参数化
    @pytest.mark.parametrize("execute_info", TestData.execute_infos, ids=TestData.ids)
    def test_appui(self, driver, execute_info):
        steps = execute_info["steps"]
        data = execute_info["examples"]
        execute(driver, steps, data)
