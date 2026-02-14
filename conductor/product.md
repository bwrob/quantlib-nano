# Initial Concept\n\nQuantLib is exposed to Python officially via SWIG. It's slow and lacks type annotations. This project aims to build alternative Python bindings using litgen and nanobind, starting with core yield curve and calendar functionality as a performance benchmark.

# Product Definition - quantlib-nano

## Vision
To provide a high-performance, modern, and fully type-annotated Python interface to the QuantLib C++ library. By leveraging `nanobind` and `litgen`, `quantlib-nano` aims to replace the existing SWIG-based bindings with a faster, more maintainable, and developer-friendly alternative that maintains 1:1 functional parity.

## Target Users
- **Quantitative Researchers & Analysts:** Requiring high-performance backtesting and financial modeling tools where execution speed is critical.
- **Financial Software Developers:** Seeking robust IDE support, type safety, and a "drop-in" replacement for the official QuantLib Python bindings.

## Core Features
- **Performance:** Significant reduction in call overhead compared to SWIG, optimized for scenarios involving many small calls (e.g., yield curve bootstrapping, daily risk calculations).
- **Type Safety:** Automated generation of comprehensive Python type hints (`.pyi` files) for superior developer experience and error detection.
- **Ease of Migration:** Designed as a drop-in replacement (`import quantlib-nano as ql`) with 1:1 functional parity with the official SWIG API.
- **Handle Pattern Support:** Transparent support for QuantLib's \`Handle<T>\` smart pointer pattern, ensuring "Pythonic" observability parity with SWIG.
- **Template & Interpolator Support:** Robust handling of C++ templates, specifically focusing on yield curve interpolators (e.g., \`Linear\`, \`LogLinear\`, \`Cubic\`) to provide full flexibility in curve construction.
- **Automated Maintenance:** Utilizing \`litgen\` to automate the binding generation process, eliminating the need for manual \`.i\` file maintenance.

## Success Metrics (Initial Phase)
- **Benchmark Performance:** Demonstrate superior execution speed in a "50-year daily discount factor" benchmark compared to official SWIG bindings.
- **API Coverage:** Successful implementation of core modules required for yield curve construction and calendar operations.
- **Handle Parity:** Successful implementation and testing of a `RelinkableHandle` to verify observability parity.
