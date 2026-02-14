lt;
                },
                arg("index") = -1,
                "Remove and return item at `index` (default last).")

          .def("extend",
               [](Vector &v, const Vector &src) {
                   v.insert(v.end(), src.begin(), src.end());
               },
               "Extend `self` by appending elements from `arg`.")

          .def("__setitem__",
               [](Vector &v, Py_ssize_t i, const Value &value) {
                   v[detail::wrap(i, v.size())] = value;
               })

          .def("__delitem__",
               [](Vector &v, Py_ssize_t i) {
                   v.erase(v.begin() + detail::wrap(i, v.size()));
               })

          .def("__getitem__",
               [](const Vector &v, const slice &slice) -> Vector * {
                   auto [start, stop, step, length] = slice.compute(v.size());
                   auto *seq = new Vector();
                   seq->reserve(length);

                   for (size_t i = 0; i < length; ++i) {
                       seq->push_back(v[start]);
                       start += step;
                   }

                   return seq;
               })

          .def("__setitem__",
               [](Vector &v, const slice &slice, const Vector &value) {
                   auto [start, stop, step, length] = slice.compute(v.size());

                   if (length != value.size())
                       throw index_error(
                           "The left and right hand side of the slice "
                           "assignment have mismatched sizes!");

                   for (size_t i = 0; i < length; ++i) {
                       v[start] = value[i];
                       start += step;
                    }
               })

          .def("__delitem__",
               [](Vector &v, const slice &slice) {
                   auto [start, stop, step, length] = slice.compute(v.size());
                   if (length == 0)
                       return;

                   stop = start + (length - 1) * step;
                   if (start > stop) {
                       std::swap(start, stop);
                       step = -step;
                   }

                   if (step == 1) {
                       v.erase(v.begin() + start, v.begin() + stop + 1);
                   } else {
                       for (size_t i = 0; i < length; ++i) {
                           v.erase(v.begin() + stop);
                           stop -= step;
                       }
                   }
               });
    }

    if constexpr (detail::is_equality_comparable_v<Value>) {
        cl.def(self == self, sig("def __eq__(self, arg: object, /) -> bool"))
          .def(self != self, sig("def __ne__(self, arg: object, /) -> bool"))

          .def("__contains__",
               [](const Vector &v, const Value &x) {
                   return std::find(v.begin(), v.end(), x) != v.end();
               })

          .def("__contains__", // fallback for incompatible types
               [](const Vector &, handle) { return false; })

          .def("count",
               [](const Vector &v, const Value &x) {
                   return std::count(v.begin(), v.end(), x);
               }, "Return number of occurrences of `arg`.")

          .def("remove",
               [](Vector &v, const Value &x) {
                   auto p = std::find(v.begin(), v.end(), x);
                   if (p != v.end())
                       v.erase(p);
                   else
                       throw value_error();
               },
               "Remove first occurrence of `arg`.");
    }

    return cl;
}

NAMESPACE_END(NB_NAMESPACE)