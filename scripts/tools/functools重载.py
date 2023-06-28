from functools import singledispatch


@singledispatch
def x(y):
    print(123)


@x.register(int)
def _(y):
    print('int')


@x.register(str)
def _(y):
    print('str')


# x(1)
x('1')
