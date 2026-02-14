cmake_minimum_required(VERSION 3.15...3.31)
project(quantlib_nano LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Force use of .venv Python
set(Python_EXECUTABLE "/Users/bwrob/dev/bwrob/quantlib-nano/.venv/bin/python")
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Point to nanobind manually
set(nanobind_DIR "/Users/bwrob/dev/bwrob/quantlib-nano/.venv/lib/python3.10/site-packages/nanobind/cmake")
set(nanobind_INCLUDE_DIR "/Users/bwrob/dev/bwrob/quantlib-nano/.venv/lib/python3.10/site-packages/nanobind/include")

list(APPEND CMAKE_MODULE_PATH "${nanobind_DIR}")
find_package(nanobind CONFIG REQUIRED)

# QuantLib setup
set(QUANTLIB_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/external/quantlib")
include_directories("${QUANTLIB_ROOT}")

# Include src/ for composite header
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/src")

# Boost setup
set(BOOST_ROOT "/opt/homebrew/opt/boost")
include_directories("${BOOST_ROOT}/include")
link_directories("/opt/homebrew/lib")

# QuantLib library path
link_directories("${CMAKE_CURRENT_SOURCE_DIR}/external/quantlib/build/ql")

# Gather all generated source files
file(GLOB GENERATED_SOURCES "src/generated/*.cpp")

# Define the extension module
nanobind_add_module(quantlib_nano_cpp
  NB_STATIC
  src/module.cpp
  ${GENERATED_SOURCES}
)

# Use hidden visibility
set_target_properties(quantlib_nano_cpp PROPERTIES
  CXX_VISIBILITY_PRESET hidden
  VISIBILITY_INLINES_HIDDEN ON
)

# Define NB_DOMAIN to isolate nanobind internals
target_compile_definitions(quantlib_nano_cpp PRIVATE NB_DOMAIN=quantlib_nano)

# Link against the local QuantLib
target_link_libraries(quantlib_nano_cpp PRIVATE QuantLib)
