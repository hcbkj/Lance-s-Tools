
login_flag = False

def login_verity(fn):
    def inner(*args, **kwargs):
        global login_flag
        if login_flag == False:
            # 这里完成登录的校验
            print('这里目前还没有完成登录操作')
            while True:
                username = input('>>>')
                password = input('>>>')
                if username == 'admin' and password == '123':
                    print('登录成功')
                    login_flag = True
                    break
                else:
                    print('登录失败，用户名或密码错误')

        ret = fn(*args, **kwargs)

        return ret

    return inner


@login_verity
def add():
    print('添加员工信息')


@login_verity
def delete():
    print('删除员工信息')


@login_verity
def update():
    print('修改员工信息')


@login_verity
def search():
    print('查询员工信息')


add()
delete()
update()
search()
