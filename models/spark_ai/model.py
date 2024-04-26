# -*- coding: utf-8 -*-

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from utils.DbUtil import MySQLDB
from utils.ParamValidator import ParamValidator
from utils.TextParser import SparkTextParser


class SparkAiModel:

    def get_spark_ai_content(self, params):
        # db_host = "mysql.sqlpub.com"
        # db_port = 3306
        # db_database = "ibun_mysql"
        # db_username = "ibun_mysql"
        # db_password = "FPduqVo2IABucGg1"
        #
        # # 替换以下信息为你的 MySQL 远程数据库连接信息
        # db = MySQLDB(host=db_host, port=db_port, username=db_username, password=db_password, database=db_database)
        # db.connect()
        #
        # # 参数验证
        # required_fields = ['ipaddress', 'uniqueIdentifier', 'question']
        # ParamValidator.check_params(params, required_fields)
        #
        # # 查询
        # select_condition_keys = ['ipaddress', 'uniqueIdentifier']
        # select_condition_params = SparkTextParser.filter_params(params, select_condition_keys)
        # select_condition = [f"{key} = '{value}'" for key, value in select_condition_params.items()]
        # select_conditions = " AND ".join(select_condition)
        # select_records = db.select_records('chrome_info', select_conditions)
        #
        # if select_records:
        #     data_to_update = dict()
        #     data_to_update['use_count'] = select_records[0][3] + 1
        #     update_condition = select_conditions
        #     db.update_record('chrome_info', data_to_update, update_condition)
        #
        # else:
        #
        #     # 插入示例
        #     data_to_insert = dict()
        #     data_to_insert['ipaddress'] = params['ipaddress']
        #     data_to_insert['uniqueIdentifier'] = params['uniqueIdentifier']
        #     data_to_insert['local_address'] = ""
        #     data_to_insert['use_count'] = 1
        #     # 将列表转换为 JSON 字符串
        #     data_to_insert['question'] = params['question'] if isinstance(params['question'], str) else str(
        #         params['question'])
        #
        #     db.insert_record('chrome_info', data_to_insert)
        # db.disconnect()

        # 星火认知大模型v3.5的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
        # 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
        SPARKAI_APP_ID = '520c0ed9'
        SPARKAI_API_SECRET = 'N2MzMzhkZjg4ODU0YzI0MmFjMTU2MWM2'
        SPARKAI_API_KEY = '6793b5ed25fae0ec9141e1cef590e535'
        # 星火认知大模型v3.5的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        SPARKAI_DOMAIN = 'generalv3.5'

        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )

        # messages = [ChatMessage(
        #     role="user",
        #     content='你好呀'
        # )]

        # 将 params['question'] 转换为与 messages 相同类型的数据
        question_messages = []
        for param in params['question']:
            message = ChatMessage(
                role=param['role'],
                content=param['content']
            )
            question_messages.append(message)

        handler = ChunkPrintHandler()
        content = spark.generate([question_messages], callbacks=[handler])
        # 使用工具类解析text数据
        parsed_texts = SparkTextParser.parse_text(content)

        return parsed_texts
