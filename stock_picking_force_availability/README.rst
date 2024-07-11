.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

================================
Stock Picking Force Availability
================================

This module allows you to force the availability of unavailable products from a delivery order.

To be able to force availability, two conditions must be met:

#. The status of the operation is 'Waitting'.
#. The 'Operation Type' allows to force the availability.


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure this module, you need to:

#. Go to module 'Inventory' -> 'Configuration' -> 'Operations Types'.
#. Edit or Create a new Operation Type.
#. Check the box 'Allow to Force Availability'.


Usage
=====

To use this module, you need to:

#. Create a quotation with unavailable products
#. Confirm the quotation
#. Go to the generated delivery order
#. Click on 'Force Availability' to force the availability of the products.


ROADMAP
=======

Currently, this module only allows you to force the availability of products without traceability. 
This means that it does not allow to force the availability of products with serial or lot number. 

We will consider adding them in future updates.


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-stock-logistics-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-stock-logistics-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Ángel García de la Chica Herrera <angel.garcia@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-stock-logistics-workflow <https://github.com/sygel-technology/sy-stock-logistics-workflow>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
