onst std::string &arg);

  /*
   * Insert 'Image: ...'
   */
  void handleTagImage(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Format nice param description with type information
   */
  void handleTagParam(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Format the contents of the \return tag or its synonyms.
   */
  void handleTagReturn(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Writes text for \ref tag. 
   */
  void handleTagRef(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /* Handles HTML tags recognized by Doxygen, like <A ...>, <ul>, <table>, ... */

  void handleDoxyHtmlTag(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /** Does not output params of HTML tag, for example in <table border='1'>
   * 'border=1' is not written to output.
   */
  void handleDoxyHtmlTagNoParam(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /** Translates tag <a href = "url">text</a> to: text ("url"). */
  void handleDoxyHtmlTag_A(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Handles HTML tags, which are translated to markdown-like syntax, for example
   * <i>text</i>  -->  _text_. Appends arg for start HTML tag and end HTML tag.
   */
  void handleDoxyHtmlTag2(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /* Handles HTML table, tag <tr> */
  void handleDoxyHtmlTag_tr(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /* Handles HTML table, tag <th> */
  void handleDoxyHtmlTag_th(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /* Handles HTML table, tag <td> */
  void handleDoxyHtmlTag_td(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /* Handles HTML entities recognized by Doxygen, like &lt;, &copy;, ... */
  void handleHtmlEntity(DoxygenEntity &, std::string &translatedComment, const std::string &arg);


  /*
   * Simple helper function that calculates correct parameter type
   * of the node stored in 'currentNode'
   * If param with specified name is not found, empty string is returned
   */
  std::string getParamType(std::string name);

  /*
   * Simple helper function to retrieve the parameter value
   */
  std::string getParamValue(std::string name);

private:
  // temporary thing, should be refactored somehow
  Node *currentNode;

  // Extra indent for the current paragraph, must be output after each new line.
  std::string m_indent;


  // this contains the handler pointer and one string argument
  typedef std::map<std::string, std::pair<tagHandler, std::string> >TagHandlersMap;
  static TagHandlersMap tagHandlers;

  // this contains the sections titles, like 'Arguments:' or 'Notes:', that are printed only once
  static std::map<std::string, std::string> sectionTitles;

  // Helper functions for fillStaticTables(): make a new tag handler object.
  TagHandlersMap::mapped_type make_handler(tagHandler handler);
  TagHandlersMap::mapped_type make_handler(tagHandler handler, const char *arg);

  void fillStaticTables();
};

#endif