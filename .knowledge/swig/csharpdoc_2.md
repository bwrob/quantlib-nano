es(): make a new tag handler object.
  TagHandlersMap::mapped_type make_handler(tagHandler handler);
  TagHandlersMap::mapped_type make_handler(tagHandler handler, const char *arg);

  void fillStaticTables();

  bool paramExists(std::string param);
};

#endif