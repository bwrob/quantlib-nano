### Integration tests vs unit tests

Unit tests (litgen/src/litgen/tests) will test the bindings code generation, but will not compile and test the bindings: they will compare the
generated code with a reference code (with a string comparison).

Integration tests (litgen/src/litgen/integration_tests) will compile the bindings and run them. They will test:
- that the generated code compiles to a binding library
- that the binding library can be imported in python
- that the generated bindings pass python tests

### Develop and debug integration tests

The script "src/litgen/validate_bindings_compilation/validate_bindings_compilation.py" contains a sandbox where you can:
- provide C++ sample code for which to generate bindings
- provide options for litgen
- provide python sample code that will test the generated bindings

This is a good place to develop and debug litgen, before running the full integration tests.

### Run the full integration tests

A justfile (see [just.systems](https://just.systems/)) is provided at the top of the repository (see [justfile](../../../justfile)).
It provides commands to help run the tests:

```bash
 just -l
Available recipes:
    build_integration_tests_nanobind # Builds the integration tests for nanobind
    build_integration_tests_pybind   # Builds the integration tests for pybind
    default                          # List all available commands
    integration_tests                # Runs all tests for pybind and nanobind (after building the integration tests)
    integration_tests_nanobind       # Runs all tests for nanobind, after building the integration tests
    integration_tests_pybind         # Runs all tests for pybind, after building the integration tests
    mypy                             # Runs mypy on the top level folder (see mypy.ini)
    pytest                           # Just runs pytest (requires that the integration tests have been built)
```