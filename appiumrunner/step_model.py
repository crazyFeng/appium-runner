class StepModel():
    """
    sort:操作步骤
    is_skip:判断是否需要操作
    action:操作动作（点击，写文本等）
    searchType: 定位方式(通过id,xpath)
    searchvalue: 元素值(具体的id值，xpath值等)
    searchindex:多元素下标
    validateSource:校验值来源
    validateAttr:属性名
    validateType:校验方式
    validateData:数据项
    param：参数
    desc:说明
    """

    sort = ""
    action = ""
    searchType = ""
    searchvalue = ""
    searchindex = ""
    validateSource = ""
    validateAttr = ""
    validateType =""
    validateData = ""
    desc =""