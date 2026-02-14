# Product Guidelines - quantlib-nano

## Prose and Documentation Style

- **Concise & Technical:** Documentation should focus on technical implementation details, performance characteristics, and the binding generation process.
- **Minimalist Approach:** Avoid unnecessary fluff. Assume the reader is a developer or quant familiar with QuantLib C++ or the official SWIG bindings.
- **Internal Focus:** Since this is a technical wrapper, prioritize documenting the _how_ and _why_ of the binding generation over end-user financial tutorials.

## Visual Identity

- **Utility-Focused:** Branding should be minimalist and functional.
- **Clean Aesthetic:** Use standard, well-maintained documentation themes (e.g., Sphinx with a modern, clean skin) and simple geometric design elements if a logo is needed.

## Technical & Performance Standards

- **Minimal Runtime Overhead:** The core priority is reducing the call overhead between Python and C++. Every binding decision should favor execution speed.
- **Binary Size Optimization:** Leverage `nanobind` features to keep the compiled extension modules compact.
- **Strict Type Parity:** Ensure 1:1 mapping of C++ types to Python type hints (`.pyi` files). Automated verification should be used where possible to ensure parity with the SWIG API.
