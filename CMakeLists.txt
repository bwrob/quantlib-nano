cmake_minimum_required(VERSION 3.15...3.31)
project(quantlib_nano LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find nanobind
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_VARIABLE nanobind_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_MODULE_PATH "${nanobind_DIR}")
find_package(nanobind CONFIG REQUIRED)

# QuantLib setup
# For now, we point to the submodule headers
# In later tracks, we might want to build QuantLib as part of this or find it
set(QUANTLIB_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/external/quantlib")
include_directories("${QUANTLIB_ROOT}")

# Define the extension module
nanobind_add_module(quantlib_nano_cpp
  src/module.cpp
  # The generated glue code will be added here
)

# Link QuantLib (placeholder for now as we're mostly using headers/templates)
# target_link_libraries(quantlib_nano_cpp PRIVATE QuantLib::QuantLib)
