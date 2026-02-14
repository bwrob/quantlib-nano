rtant
   * when single word commands like \c are at the end of line.
   */
  bool isEndOfLine();

  /**
   * Skips spaces, tabs, and end of line tokens.
   */
  void skipWhitespaceTokens();

  /**
   * Removes all spaces and tabs from beginning end end of string.
   */
  std::string trim(const std::string &text);

  /*
   * Returns string of the next token if the next token is PLAINSTRING. Returns
   * empty string otherwise.
   */
  std::string getNextToken();

  /*
   * Returns the next word ON THE CURRENT LINE ONLY
   * if a new line is encountered, returns a blank std::string.
   * Updates the iterator if successful.
   */
  std::string getNextWord();

  /*
   * Returns the next word, which is not necessarily on the same line.
   * Updates the iterator if successful.
   */
  std::string getNextWordInComment();

  /* 
   * Returns the location of the end of the line as
   * an iterator.
   */
  TokenListCIt getOneLine(const TokenList &tokList);

  /*
   * Returns a properly formatted std::string
   * up til ANY command or end of line is encountered.
   */
  std::string getStringTilCommand(const TokenList &tokList);

  /*
   * Returns a properly formatted std::string
   * up til the command specified is encountered
   */
  //TODO check that this behaves properly for formulas
  std::string getStringTilEndCommand(const std::string &theCommand, const TokenList &tokList);

  /*
   * Returns the end of a Paragraph as an iterator-
   * Paragraph is defined in Doxygen to be a paragraph of text
   * separated by either a structural command or a blank line
   */
  TokenListCIt getEndOfParagraph(const TokenList &tokList);

  /*
   * Returns the end of a section, defined as the first blank line OR first
   * encounter of the same command. Example of this behaviour is \arg.
   * If no end is encountered, returns the last token of the std::list.
   */
  TokenListCIt getEndOfSection(const std::string &theCommand, const TokenList &tokList);

  /*
   * This method is for returning the end of a specific form of doxygen command
   * that begins with a \command and ends in \endcommand
   * such as \code and \endcode. The proper usage is
   * progressTilEndCommand("endcode", tokenList);
   * If the end is never encountered, it returns the end of the std::list.
   */
  TokenListCIt getEndCommand(const std::string &theCommand, const TokenList &tokList);
  /*
   * A special method for commands such as \arg that end at the end of a
   * paragraph OR when another \arg is encountered
  //TODO getTilAnyCommand
  TokenListCIt getTilAnyCommand(const std::string &theCommand, const TokenList &tokList);
   */

  /**
   * This methods skips end of line token, if it is the next token to be
   * processed. It is called with comment commands which have args till the
   * end of line, such as 'addtogroup' or 'addindex'.
   * It is up to translator to specific language to decide whether
   * to insert eol or not. For example, if a command is ignored in target
   * language, new lines may make formatting ugly (Python).
   */
  void skipEndOfLine();

  /*
   * Method for Adding a Simple Command
   * Format: @command
   * Plain commands, such as newline etc, they contain no other data
   *  \n \\ \@ \& \$ \# \< \> \% \{ \}
   */
  void addSimpleCommand(const std::string &theCommand, DoxygenEntityList &doxyList);
  /*
   * CommandWord
   * Format: @command <word>
   * Commands with a single WORD after then such as @b
   * "a", "b", "c", "e", "em", "p", "def", "enum", "example", "package", 
   * "relates", "namespace", "relatesalso","anchor", "dontinclude", "include",
   * "includelineno"
   */
  void addCommandWord(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * CommandLine
   * Format: @command (line)
   * Commands with a single LINE after then such as @var
   * "addindex", "fn", "name", "line", "var", "skipline", "typedef", "skip",
   * "until", "property"
   */
  void addCommandLine(const std::string &theCommand, c