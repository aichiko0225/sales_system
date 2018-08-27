from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class ResponseModel(object):
    """
    restful API
    统一返回的Model
    """
    
    code: int  # 0 为成功 1 为失败
     
    message: str

    def __init__(self, **kwargs: dict):
        code = kwargs.get('code')
        self.code = code
        message = kwargs.get('message')
        self.message = message
        data = kwargs.get('data')
        self.data = data

    def __repr__(self):
        if isinstance(self.data, object):
            return '<ResponseModel>(code = %s, message = %s) data = %s' % (self.code, self.message, self.data.__dict__)
        else:
            return '<ResponseModel>(code = %s, message = %s) data = %s' % (self.code, self.message, self.data)
