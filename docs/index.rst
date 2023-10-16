Home Assistant 2 Excel
======================

Usage is super simple.

1. Install homeassistant2xlsx:

.. code:: bash

    pip3 install homeassistant2xlsx

2. Create a Excel Workbook with any number of sheets.
   Add any Home Assistant entity name as comment in the cells of the **first** row.
   Entities are stored as string by default.
   Optionally, append ``|int`` or ``|float`` for a corresponding conversion.
   Use ``date``, ``time`` or ``datetime`` for the corresponding timestamps.

    .. image:: static/spreadsheet1.png

3. Go to your Home Assistant instance and create a Long-Live API Token.
4. Run ``homeassistant2xlsx``

.. code:: bash

    homeassistant2xlsx --host localhost --token YOUR_API_TOKEN  my.xlsx

Command Line Interface
----------------------

.. literalinclude:: static/cli.txt
   :language: text


API
---

.. toctree::
    api/homeassistant2xlsx