Home Assistant 2 Excel
======================


.. contents::
   :depth: 1
   :local:


Getting Started
---------------

Usage is super simple.

1.  Install homeassistant2xlsx

    .. code:: bash

        pip3 install homeassistant2xlsx

2.  Create a Excel Workbook with any number of sheets.
    Add any Home Assistant entity name as comment of the **first** row,
    ``sensor.gas`` for example.
    Home Assistant stores entities as string by default.
    Optionally, append ``|int`` or ``|float`` for a corresponding conversion.
    ``sensor.gas|int`` or ``sensor.gas|float`` for example.

    .. image:: static/spreadsheet1.png

    The comments (aka entity names) ``date``, ``time`` or ``datetime`` provide the corresponding timestamps.


3.  Go to your Home Assistant instance and create a Long-Live API Token.
4.  Run ``homeassistant2xlsx``

    .. code:: bash

        homeassistant2xlsx --host localhost --token YOUR_API_TOKEN  my.xlsx

Command Line Interface
----------------------

.. literalinclude:: static/cli.txt
   :language: text


Programming Interface
---------------------

.. automodule:: homeassistant2xlsx
   :members:
   :undoc-members:
   :show-inheritance:

Links
-----

- `PyPI - Python Package Index <https://pypi.org/project/homeassistant2xlsx/>`_
- `Source Code <https://github.com/c0fec0de/homeassistant2xlsx>`_
- `Issues <https://github.com/c0fec0de/homeassistant2xlsx/issues>`_
