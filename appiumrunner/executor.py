import operator
import time
import uuid

from selenium.common.exceptions import NoSuchElementException


def execute(driver, steps, data):
    """
    执行用例
    :param driver:
    :param steps: 具体步骤
    :param data: 数据项
    :return: None
    """
    for step in steps:
        time.sleep(1)
        # 无需元素的动作
        if step.action == 'screenshot':
            filename = uuid.uuid1().hex
            r = driver.get_screenshot_as_file(
                'static/screenshot/' + filename + '.png')  # 截图

        elif step.action == 'wait':  # 等待
            time_value = data[step.validateData]
            time.sleep(int(time_value))
            # WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(element))
            # driver.implicitly_wait(int(step.validateData))
        elif step.action == 'end':  # 步骤执行结束
            driver.close_app()
            time.sleep(1)
            driver.launch_app()
            continue
        # 找到元素
        element = None
        try:
            if step.searchType == 'find_elements_by_id':
                element = getattr(driver, step.searchType)(
                    step.searchvalue)[step.searchIndex]
            elif step.action == 'wait':
                continue
            else:
                element = getattr(driver, step.searchType)(
                    step.searchvalue)
        except NoSuchElementException:
            print("找不到对应的元素，定位方式为:{}，定位值为：{}".format(step.searchType, step.searchvalue))

        assert not element is None, "元素没有定位到，不能为空！"

        # 执行动作
        if step.action == 'assert':  # 断言
            value = None
            if step.validateSource == 'normal':
                value = element.text  # 获取内容
            else:
                value = getattr(element, 'get_attribute')(step.validateAttr)

            assertResult = True  # 断言结果

            if step.validateType == 'contains':  # 包含
                assertResult = value.__contains__(
                    step.validateData)
            elif step.validateType == 'equals':  # 相同
                assertResult = value == step.validateData
            else:
                assertResult = getattr(operator, step.validateType)(
                    float(value), float(step.validateData))
            assert assertResult,"断言不通过"

        elif step.action == 'send_keys':  # 输入文字
            keys_value = data[step.validateData]
            getattr(element, step.action)(keys_value)

        else:
            getattr(element, step.action)()
