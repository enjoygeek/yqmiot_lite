# -*- encoding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import controller

def run():
    controller.run()