from xlrd import open_workbook
from appiumrunner.step_model import StepModel as model


class ExcelReader():

    @staticmethod
    def read_excel(excel_path):

        reader = open_workbook(excel_path)
        names = reader.sheet_names()

        # 1. 读取步骤，以列表保存 {"login":[step1,step2]}
        step_dict = {}
        for name in names:
            if name == 'data':
                continue;
            step_dict[name] = []

            case_xls = reader.sheet_by_name(name)
            for i in range(case_xls.nrows):
                if i == 0:  # 跳过表头
                    continue
                smart_list = []  # 一个集合代表一个步骤
                for j in range(case_xls.ncols):
                    smart_list.append(case_xls.cell(i, j).value)
                mode = model()
                mode.sort = smart_list[0]
                mode.desc = smart_list[1]
                mode.action = smart_list[2]
                mode.searchType = smart_list[3]
                mode.searchvalue = smart_list[4]
                mode.searchindex = smart_list[5]
                mode.validateSource = smart_list[6]
                mode.validateAttr = smart_list[7]
                mode.validateType = smart_list[8]
                mode.validateData = smart_list[9]
                step_dict[name].append(mode)  # [mode1.model2 mode3 ]

        # 2. 读取数据，以列表保存 {"login":[data1,data2]}
        data_dict = {}
        data_xls = reader.sheet_by_name("data")
        for i in range(data_xls.nrows):
            name = data_xls.cell(i, 0).value
            data_dict[name] = []

            for j in range(data_xls.ncols):
                value = data_xls.cell(i, j).value.strip()
                if (j == 0) or (value == ""):
                    continue
                data_dict[name].append(eval(value))

        # 3. 格式转变 [{name,desc,examples,steps}]
        result = []
        for case_name in list(step_dict.keys()):
            if data_dict[case_name]:
                data_list = data_dict[case_name]
                num = 0
                for data in data_list:
                    result.append({
                        "name": case_name,
                        "steps": step_dict[case_name],
                        "examples": data,
                        "desc": "{}_{}".format(case_name, num)
                    })
                    num += 1

            else:
                result.append({
                    "name": case_name,
                    "steps": step_dict[case_name],
                    "examples": {},
                    "desc": "{}_0".format(case_name)
                })

        return result
