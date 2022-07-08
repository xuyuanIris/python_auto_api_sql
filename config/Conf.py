import os


class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = "./testcase/"

    # 执行方式（jenkins/local）
    exe_mode = 'local'

    # 测试环境（测试/正式）
    test_env_config = '测试'

    # 项目名称(给报告文件使用，使用properties文件不支持中文，xml文件可以)
    project_name = '宁夏登记系统统计分析'

    # 报告title
    report_title = f'宁夏登记系统（{test_env_config}环境）接口测试报告'

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "100"

    # 保留最多报告数
    report_number_max = "1"

    # 日志级别（CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET）
    log_level = 'INFO'

    # 日志是否开启控制台输出
    log_out_console = True

    # 获取测试数据方式(mysql/excel)
    test_data_type = "excel"

    # 是否发送企业微信通知（是 1 ，否 0）
    send_wx_message = 0

    # 企业微信机器人地址
    send_wx_message_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9dc2252b-8c96-4462-8dd3-e32ef2d74719'

    # 流程用例使用测试数据表名
    # test_data_p_table = 'estate_nmst_internet_process_data'
    test_data_p_table = 'estate_nmst_process_data'

    # 模块用例使用测试数据表名
    # test_data_m_table = 'estate_nmst_internet_module_data'
    test_data_m_table = 'estate_nmst_module_data'

    # 是否使用本地缓存文件(是 1 ，否 0 ，使用框架内缓存 2)
    test_user_cache = 0

    # 本地用户缓存目录（使用本地缓存时生效）
    # test_user_cache_dir = r'D:\testfile\hn'
    test_user_cache_dir = r'/Users/xuyuan/Documents/TYHTWork/auto_estate_hn_web/hn'


class PathConfig:
    """
    通用地址配置
    """
    _path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 是否是windows/mac系统
    sysname = "mac"

    if(sysname == "windows"):

        # 用例目录
        testcase = _path + "\\testcase"

        # 测试数据本地地址
        test_data = _path + "\\testcase\\data"

        # log
        log = _path + '\\logs'

        # report
        report = _path + '\\report'

        # lib目录
        lib = _path + "\\lib"

        # 导出文件存放目录
        export = _path + "\\lib\\export"

        # 截图文件保存地址目录
        screenshot = _path + "\\lib\\screenshot"

        # 图片二维码识别文件目录
        tpyzm = _path + "\\lib\\tpyzm"

        # 上传文件目录
        upload = _path + "\\lib\\upload"
    else:
        # 用例目录
        testcase = _path + "/testcase"

        # 测试数据本地地址
        test_data = _path + "/testcase/data"

        # log
        log = _path + '/logs'

        # report
        report = _path + '/report'

        # lib目录
        lib = _path + "/lib"

        # 导出文件存放目录
        export = _path + "/lib/export"

        # 截图文件保存地址目录
        screenshot = _path + "/lib/screenshot"

        # 图片二维码识别文件目录
        tpyzm = _path + "/lib/tpyzm"

        # 上传文件目录
        upload = _path + "/lib/upload"
