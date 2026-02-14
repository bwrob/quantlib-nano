e, than the contents of the tag
   * arg - message
   */
  void handleTagMessage(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

  /*
   * Insert <img src=... /> tag if the 'format' field is specified as 'html'
   */
  void handleTagImage(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

  /*
   * Insert <p alt='title'>...</p>
   */
  void handleTagPar(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

  /*
   * Insert \@param command, if it is really a function param
   */
  void handleTagParam(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

  /*
   * Writes link for \ref tag. 
   */
  void handleTagRef(DoxygenEntity &tag, std::string &translatedComment, std::string &);

  /*
   * Insert {@link...} command, and handle all the <link-object>s correctly
   * (like converting types of params, etc)
   */
  void handleTagLink(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

  /*
   * Insert @see command, and handle all the <link-object>s correctly
   * (like converting types of params, etc)
   */
  void handleTagSee(DoxygenEntity &tag, std::string &translatedComment, std::string &arg);

private:
  Node *currentNode;
  // this contains the handler pointer and one string argument
  static std::map<std::string, std::pair<tagHandler, std::string> > tagHandlers;
  void fillStaticTables();

  bool paramExists(std::string param);
  std::string indentAndInsertAsterisks(const std::string &doc);

  void addError(int warningType, const std::string &message);
};

#endif