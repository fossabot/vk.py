.. vk.py documentation master file, created by
   sphinx-quickstart on Sun Sep 22 02:54:36 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vk.py's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
.. figure:: https://user-images.githubusercontent.com/28061158/63603699-cd51b980-c5d2-11e9-8a8f-06e1eef20afe.jpg
   :alt: vk.py


   Fastest, scalable, fully asynchronous.


Install
-------

Newest version.

.. code:: sh

   pip install https://github.com/prostomarkeloff/vk.py/archive/master.zip --upgrade

Stable version.

.. code:: sh

   pip install vk.py

Usage
-----

A simple example

.. code:: python

   from vk import VK
   from vk.utils.task_manager import TaskManager
   import logging

   logging.basicConfig(level="INFO")
   vk = VK(access_token=<TOKEN>)

   async def status_get():
       resp = await vk.api_request("status.get")
       print(resp)

   if __name__ == "__main__":
       task_manager = TaskManager(vk.loop)
       task_manager.add_task(status_get)
       task_manager.run()

You can find more examples on github.

Features
--------

-  Rich high-level API.
-  Fully asynchronous. Based on asyncio and aiohttp.
-  Bot framework out of-the-box.
-  Fully typed, thanks to Pydantic.
-  Compatible with PyPy.
-  Have a lot of tools (in bot framework) out-of-the-box for creating
   largest and powerful applications
   `click <reference/vk.bot_framework.addons>`__:

   -  Caching
   -  Blueprints
   -  Cooldowns
   -  FSM (WIP)

Alternatives
------------

-  Kutana. Bot engine for creating Telegram and VK bots
-  VKBottle. Bot framework for VK bot development.
-  VK_API. A simple library for accessing VK API.

And many other libraries…


.. toctree::
   :maxdepth: 2

   You can find more here
   VK main object <reference/vk>
   Bot Framework <reference/vk.bot_framework>

   VK <reference/modules>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
