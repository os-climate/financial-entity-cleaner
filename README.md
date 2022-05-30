# financial-entity-cleaner
The financial-entity-cleaner is a library that is part of the Entity-Matching project developed by OS-Climate Foundation. The main purpose of the financial-cleaner is to provide methods for validation and standardization of data used in the banking industry as to solve the problem of determining if two entities in a data set refer to the same real-world object (entity matching).

Currently, the library provides three main components:
- a validator for banking identifiers (Sedol,Isin and Lei),
- a validator for country information, and 
- a cleaner for company's name.

## Install from PyPi

```
pip install financial-entity-cleaner
```

## How to use the library

The following jupyter notebooks teaches how to use the library:

- [How to clean a company's name](notebooks/how-to/Clean%20a%20company's%20name.ipynb)
- [How to normalize country information](notebooks/how-to/Normalize%20country%20information.ipynb)
- [How to validate banking ids, such as: LEI, ISIN and SEDOL](notebooks/how-to/Validate%20banking%20IDs.ipynb)
