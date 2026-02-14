);

        cl.def("update", [](Map &m, const Map &m2) {
            for (auto &kv : m2)
                detail::map_set<Map, Key, Value>(m, kv.first, kv.second);
        },
        "Update the map with element from `arg`");
    }

    if constexpr (detail::is_equality_comparable_v<Map>) {
        cl.def(self == self, sig("def __eq__(self, arg: object, /) -> bool"))
          .def(self != self, sig("def __ne__(self, arg: object, /) -> bool"));
    }

    // Item, value, and key views
    struct KeyView   { Map &map; };
    struct ValueView { Map &map; };
    struct ItemView  { Map &map; };

    class_<ItemView>(cl, "ItemView")
        .def("__len__", [](ItemView &v) { return v.map.size(); })
        .def("__iter__",
             [](ItemView &v) {
                 return make_iterator<Policy>(type<Map>(), "ItemIterator",
                                              v.map.begin(), v.map.end());
             },
             keep_alive<0, 1>());

    class_<KeyView>(cl, "KeyView")
        .def("__contains__", [](KeyView &v, const Key &k) { return v.map.find(k) != v.map.end(); })
        .def("__contains__", [](KeyView &, handle) { return false; })
        .def("__len__", [](KeyView &v) { return v.map.size(); })
        .def("__iter__",
             [](KeyView &v) {
                 return make_key_iterator<Policy>(type<Map>(), "KeyIterator",
                                                  v.map.begin(), v.map.end());
             },
             keep_alive<0, 1>());

    class_<ValueView>(cl, "ValueView")
        .def("__len__", [](ValueView &v) { return v.map.size(); })
        .def("__iter__",
             [](ValueView &v) {
                 return make_value_iterator<Policy>(type<Map>(), "ValueIterator",
                                                    v.map.begin(), v.map.end());
             },
             keep_alive<0, 1>());

    cl.def("keys",   [](Map &m) { return new KeyView{m};   }, keep_alive<0, 1>(),
           "Returns an iterable view of the map's keys.");
    cl.def("values", [](Map &m) { return new ValueView{m}; }, keep_alive<0, 1>(),
           "Returns an iterable view of the map's values.");
    cl.def("items",  [](Map &m) { return new ItemView{m};  }, keep_alive<0, 1>(),
           "Returns an iterable view of the map's items.");

    return cl;
}

NAMESPACE_END(NB_NAMESPACE)