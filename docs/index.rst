ModernGL.ext.obj
================

`ModernGL <https://moderngl.readthedocs.io>`_ extension for loading obj files.

- `ModernGL.ext.obj on Github <https://github.com/cprogrammer1994/ModernGL.ext.obj>`_
- `ModernGL.ext.obj on PyPI <https://pypi.python.org/pypi/ModernGL.ext.obj>`_

Install
-------

.. code-block:: sh

	pip install ModernGL.ext.obj

Usage
-----

.. code-block:: python

	import ModernGL
	from ModernGL.ext import obj

Example
-------

.. code-block:: python

	# example goes here

Documentation
-------------

.. currentmodule:: ModernGL.ext.obj

.. autoclass:: Obj

	.. automethod:: open(filename) -> Obj
	.. automethod:: frombytes(data) -> Obj
	.. automethod:: fromstring(data) -> Obj
	.. automethod:: pack(packer=default_packer) -> bytes

.. toctree::
   :maxdepth: 2
