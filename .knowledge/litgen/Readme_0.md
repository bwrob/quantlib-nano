# litgen integration tests

This folder contains a full suite of integration tests for litgen.
- It builds a native C++ library called "mylib"
- It builds a python binding library called "lg_mylib" (with a corresponding pip package name "lg-mylib")

You can install the "lg-mylib" pip package with:
```bash
pip install [-e] .
```

## List of tests and documentation

The different tests are available at [mylib/](mylib/include/mylib).

It is advised to read the different header files inside [mylib/](mylib/), since they are thoroughly
commented and can help understand litgen.
