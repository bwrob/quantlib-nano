#include <nanobind/nanobind.h>
#include "generated/registration.h"

namespace nb = nanobind;

NB_MODULE(quantlib_nano_cpp, m) {
    gen_bindings(m);
}
