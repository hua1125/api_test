
'''
主要用于所有接口的公共功能，使用一个基类（父类）。
功能1:处理URL
功能2：重新封装get，post方法
功能3：处理头信息
功能4：登录
'''
from setting import BASE_URL,LOGIN_INFO
import requests
from loguru import logger
from cacheout import Cache

cache = Cache()#创建cache对象
#创建父类
class Base():

    #实现url的拼接
    def get_url(self,path,params=None):
        '''

        path:接口路径（如：/admin/auth/login）
        params：查询参数（如：?page=1&limit=20&sort=add_time&order=desc）
        返回一个完整的url
        :return:
        '''
        if params:
            full_url = BASE_URL+path+params
            return full_url
        return BASE_URL+path
    #重写get方法
    def get(self,url):
        result = None
        response = requests.get(url,headers=self.get_headers())
        try:
            result = response.json()
            logger.success('请求URL：{}，返回结果：{}'.format(url,result))
            return result
        except Exception as e:
            logger.error('请求get方法异常：{}'.format(result))


    #重写post方法
    def post(self,url,data):
        '''

        在原来post方法的基础上，新增日志以及直接返回接送格式
        :return:
        '''
        result = None
        response = requests.post(url,json=data,headers=self.get_headers())
        try:
            result = response.json()
            logger.success('请求URL：{}，请求参数：{}，返回结果：{}'.format(url,data,result))
            return result
        except Exception as e:
            logger.error('请求post方法异常：{}'.format(result))

    #实现所有头信息的处理
    def get_headers(self):
        '''

        :return: 返回的是字典格式的请求头，多是包括Content-Type，X-Litemall-Admin-Token
        '''
        headers = {'Content-Type':'application/json'}
        token = cache.get('token')#从缓存中获取token
        if token:
            headers.update({'X-Litemall-Admin-Token':token})
            return headers
        return headers





    #实现登录功能
    def login(self):
        '''
        通过钓鱼扽了接口获取token值，将其进行缓存，其他接口使用时直接从缓存中取数，若没有渠道再调用登录
        再将token值放在缓存中
        :return:
        '''
        login_path = '/admin/auth/login'
        login_url = self.get_url(login_path)#拼接登录接口地址
        result = self.post(login_url,LOGIN_INFO)  #请求登录接口，返回接送数据
        try:
            if 0 == result.get('errno'):
                logger.success('请求登录接口成功')
                token = result.get('data').get('token')
                cache.set('token',token)
            else:
                logger.error('登录失败：{}'.format(result))
                return None
        except Exception as e:
            logger.error('请求登录接口返回异常，异常数据：{}'.format(result))
            logger.error('报错信息：{}'.format(e))




if __name__ == '__main__':
    base = Base()
    # # print(base.get_url("/admin/auth/login"))
    # login_url = base.get_url('/admin/auth/login')
    # login_data = {'username':'admin123','password':'admin123'}
    # print(base.post(login_url,login_data))
    base.login()



