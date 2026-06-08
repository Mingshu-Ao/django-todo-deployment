from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/yuanyuyu/TSDT.git'  # 代码仓库地址

def deploy():
    """主部署函数，按顺序执行所有部署步骤"""
    site_folder = f'/home/{env.user}/sites/{env.host}'  # 站点根目录
    source_folder = site_folder + '/source'  # 源代码目录
    
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    """创建必要的目录结构，已存在的目录不会报错"""
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    """从Git仓库获取最新代码"""
    if exists(source_folder + '/.git'):
        # 如果已经是Git仓库，执行fetch获取最新提交
        run(f'cd {source_folder} && git fetch')
    else:
        # 如果不是Git仓库，执行clone
        run(f'git clone {REPO_URL} {source_folder}')
    
    # 获取本地当前最新的commit哈希，并强制服务器端同步到此版本
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
    """更新Django配置文件：关闭DEBUG、设置ALLOWED_HOSTS、生成SECRET_KEY"""
    settings_path = source_folder + '/notes/settings.py'
    
    # 关闭DEBUG模式
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    
    # 设置ALLOWED_HOSTS为当前站点域名/IP
    sed(settings_path,
        r'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    
    # 生成并导入SECRET_KEY
    secret_key_file = source_folder + '/notes/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    
    # 在settings.py末尾添加导入SECRET_KEY的语句
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    """创建或更新Python虚拟环境并安装依赖"""
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        # 如果虚拟环境不存在，创建新的
        run(f'python3.9 -m venv {virtualenv_folder}')
    # 安装requirements.txt中的所有依赖
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    """收集Django静态文件"""
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_folder):
    """执行Django数据库迁移"""
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

if __name__ == "__main__":
    # 注意：这行代码是在Python脚本内部调用fab命令
    # 不建议直接这样使用，正确方式是在终端中直接执行fab命令
    # local('fab -f /path/fabfile.py deploy')
    pass