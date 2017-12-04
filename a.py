# -*- coding: utf-8 -*-

def handler(func):
    def __decorator():
        print('enter the login')
        func('2')
        print('exit the login')
    return __decorator


@handler
def test(num=None):
    print('1' + num)


test()
