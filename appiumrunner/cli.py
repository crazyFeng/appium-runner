import sys,os
import pytest
from appiumrunner.pytest_config import ConfigPlugin

def main():
    # 获取 python运行参数
    # 1. 找到 --config，读取yaml配置
    config_path = ""
    for arg in sys.argv:
        if arg.startswith("--config="):
            config_path = arg.replace("--config=", "")
    if config_path == "":
        config_path = "config.yaml"

    print(os.path.dirname(__file__))

    # 2. 构建pytest参数
    test_path = "{}/test_runner.py::TestMain::test_appui".format(os.path.dirname(__file__))
    pytest_args = ["-s", "-v", test_path, "--capture=sys", "--html=./report/report.html",
                   "--self-contained-html"]
    pytest_args.append("--config=" + config_path)
    print("run pytest：" , pytest_args)

    pytest.main(pytest_args, plugins=[ConfigPlugin()])

if __name__ == "__main__":
    main()