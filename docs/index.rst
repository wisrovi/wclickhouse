wclickhouse Documentation
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   api_reference

Introduction
------------

**wclickhouse** is a high-performance ClickHouse ORM for Python using **Pydantic v2** and **clickhouse-connect**.

Features
~~~~~~~~

* **Pydantic v2 Integration**: Define your ClickHouse tables as Pydantic models.
* **Auto-Sync**: Automatically creates tables and syncs schema.
* **Dual API**: Full support for both Synchronous and Asynchronous operations.
* **Bulk Insert Optimized**: Built-in support for efficient bulk insertions.

API Reference
-------------

.. automodule:: wclickhouse
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: wclickhouse.core.repository
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: wclickhouse.core.sync
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: wclickhouse.builders.query_builder
   :members:
   :undoc-members:
   :show-inheritance:
