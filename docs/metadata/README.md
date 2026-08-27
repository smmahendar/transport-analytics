# Metadata Framework

The metadata framework provides a scalable, consistent foundation for metadata
integration and data lineage across Transport Analytics.

Native OpenMetadata connectors are preferred wherever they cover a platform's
metadata and lineage requirements. Python components will fill the metadata and
lineage gaps that native connectors do not address.

The initial lineage path is:

`NiFi → ZIP → TXT → raw table → conformed Iceberg table`

Implementation will proceed incrementally, adding connectivity, extraction,
mapping, publishing, lineage processing, and state management in later changes.
