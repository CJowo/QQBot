# ImageSearch搜图配置

"""设置代理
default: None
example:
'http://proxy.com'
'http://user:pass@some.proxy.com'
"""
async def PROXY():
    return None


"""saucenaoAPI-KEY
saucenao注册账号后获取的API-KEY
default: ''
"""
SAUCENAO_KEY = ''


"""搜图引擎开关
"""
SAUCENAO = True
ASCII2D = True


"""缩略图显示
需要酷Qpro
"""
SHOW_IMAGE = True


"""百度图像审核
需开启缩略图显示
"""
IMAGE_CENSOR = False


"""百度审核配置(未完成)
详见: https://ai.baidu.com/ai-doc/ANTIPORN/tk3h6xgkn#%E6%96%B0%E5%BB%BAaipimagecensor
"""
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''


"""图片显示等级(未完成)
1 - 仅显示合规
2 - 显示疑似和合规
3 - 全部显示
"""
CENSOR_LEVEL = 1


"""图像审核请求错误时动作(未完成)
例如连接异常，达到限额，审核失败等
需开启百度图像审核
0 - 显示图片
1 - 不显示图片
2 - 显示错误信息
defualt: 1
"""
CENSOR_FAIL = 1


"""智能匹配(未完成)
开启后计算各个结果相似度，返回一个相似度最高的结果
关闭则返回全部结果
"""
SMART = False


"""结果缓存时间(秒)
设为0关闭结果缓存
default: 86400
"""
CACHE_TIME = 86400
