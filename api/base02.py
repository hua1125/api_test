'''
1创建一个父类
2拼接url
3重新封装get方法
4重新封装post方法
5获取headers
6登录
'''
from setting import BASE_URL,LOGIN_INFO
import requests
from loguru import logger
from cacheout import Cache
cache = Cache()


class BASE():


    #拼接url
    def get_url(self,path,params=None):

        if params:
            full_url = BASE_URL+path+params
            return full_url
        return BASE_URL+path
    #重新封装get
    def get(self,url):
        result = None
        response = requests.get(url,headers=self.get_headers())
        try:
            result = response.json()
            logger.success('请求url{},返回结果{}'.format(url,result))
            return result
        except Exception as e:
            logger.error('请求失败，返回结果{}'.format(result))
            return result


    # 重新封装post
    def post(self,url,data):
        result = None
        response = requests.post(url,json=data,headers=self.get_headers())
        try:
            result = response.json()
            logger.success('请求url{}，请求数据{}，返回结果{}'.format(url,data,result))
            return result
        except Exception as e:
            logger.error('请求失败，返回结果{}'.format(result))
            return result
    #获取headers
    def get_headers(self):
        headers = {'Content-Type':'application/json'}
        token = cache.get('token')
        if token:
            headers.update({'X-Litemall-Admin-Token':token})
            return headers
        return headers



    #登录
    def login(self):
        login_path = '/admin/auth/login'
        login_url= self.get_url(login_path)
        result = self.post(login_url,LOGIN_INFO)
        try:
            if 0 == result.get('errno'):
                logger.success('请求成功')
                token = result.get('data').get('token')#获取token
                cache.set('token',token)#将token值放入缓存
            else:
                logger.error('请求失败')
                return None
        except Exception as e:
            logger.error('报错信息{}'.format(e))

if __name__ == '__main__':
    base = BASE()
    print(base.login())
