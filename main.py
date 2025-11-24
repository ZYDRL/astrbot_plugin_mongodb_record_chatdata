from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from pymongo import MongoClient
import time
import re

@register("astrbot_plugin_mongodb_record_chatdata", "ZYDRL", "一个简单的记录聊天内容的插件，使用mongodb", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def get_record_event_message(self, event: AstrMessageEvent):
        """这是一个连接到mongodb数据库，记录聊天内容的插件""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        message_str = event.message_str  # 获取消息的纯文本内容
        if message_str is not "":
            msg = event.message_obj
            tsmp = msg.timestamp
            ts = time.localtime(tsmp) #获取消息时间
            ts = time.strftime("%Y-%m-%d %H:%M:%S", ts)
            session_id = msg.session_id
            user_name = event.get_sender_name()
            message = [{"time":ts,"session_id":session_id,"user_name":user_name,"message":message_str}]

            url = "mongodb://localhost:27017/" #写入MongoDB
            client = MongoClient(url)
            db = client["PRIVATE_MESSAGE"]
            collection = db[user_name]
            collection.insert_many(message)
            logger.info(f"已记录消息【{ts}|<{session_id}>{user_name}: {message_str}】")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
