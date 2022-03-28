## EmploymentCommunityServer
#### 基于Python3.8+FastApi+Mysql+Redis开发的纯异步后端  
   
#### 1. 核心库要求:  
- **python==3.8**
- **fastapi==0.73.0**
- **aiomysql==0.0.22**  
- **aioredis==2.0.1**
- SQLAlchemy==1.4.31
- pydantic==1.9.0  
  
#### 2. 依赖安装
```shell
# 以下脚本在项目目录中运行

# 创建虚拟环境
python -m venv venv

# 进入虚拟环境-Linux
source venv/bin/activate  
# 进入虚拟环境-Windows
 .\venv\Scripts\activate
 
 #安装依赖
pip install -r requirements.txt
```

#### 3. 本地运行  
```shell
# 建议配置正确的解释器, 使用pycharm运行,这样会有色彩区分, 且不会出现乱码
# 使用默认的uvicorn配置运行
python main.py

# 自定义uvicorn运行-可加其他参数,详见uvicorn
uvicorn main:app

# 使用Gunicorn运行-仅Linux可用
# 使用Gunicorn前需安装
pip install "uvicorn[standard]" gunicorn
## 使用Gunicorn运行
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

#### 4. 配置文件
配置文件configs.py中可设置默认值, 若.env文件或环境变量中有同名配置, 
则以环境变量为准,建议默认值设为测试环境配置, 正式服务器中