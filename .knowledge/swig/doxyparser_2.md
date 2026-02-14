onst TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * CommandParagraph
   * Format: @command {paragraph}
   * Commands with a single paragraph after then such as @return
   * "return", "remarks", "since", "test", "sa", "see", "pre", "post",
   * "details", "invariant", "deprecated", "date", "note", "warning",
   * "version", "todo", "bug", "attention", "brief", "arg", "author"
   */
  void addCommandParagraph(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * Command EndCommand
   * Format: @command and ends at @endcommand
   * Commands that take in a block of text such as @code:
   * "code", "dot", "msc", "f$", "f[", "f{environment}{", "htmlonly",
   * "latexonly", "manonly", "verbatim", "xmlonly", "cond", "if", "ifnot",
   * "link"
   * Returns 1 if success, 0 if the endcommand is never encountered.
   */
  void addCommandEndCommand(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * CommandWordParagraph
   * Format: @command <word> {paragraph}
   * Commands such as param
   * "param", "tparam", "throw", "throws", "retval", "exception"
   */
  void addCommandWordParagraph(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * CommandWordLine
   * Format: @command <word> (line)
   * Commands such as param
   * "page", "subsection", "subsubsection", "section", "paragraph", "defgroup"
   */
  void addCommandWordLine(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * Command Word Optional Word Optional Word
   * Format: @command <word> [<header-file>] [<header-name>]
   * Commands such as class
   * "category", "class", "protocol", "interface", "struct", "union"
   */
  void addCommandWordOWordOWord(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);
  /*
   * Command Optional Word
   * Format: @command [<word>]
   * Commands such as dir
   * "dir", "file", "cond"
   */
  void addCommandOWord(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  /*
   * Commands that should not be encountered (such as PHP only)
   * goes til the end of line then returns
   */
  void addCommandErrorThrow(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  void addCommandHtml(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  void addCommandHtmlEntity(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  /*
   *Adds the unique commands- different process for each unique command
   */
  void addCommandUnique(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  /*
   * Replace the given command with its predefined alias expansion.
   */
  void aliasCommand(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  /*
   * Simply ignore the given command, possibly with the word following it or
   * until the matching end command.
   */
  void ignoreCommand(const std::string &theCommand, const TokenList &tokList, DoxygenEntityList &doxyList);

  /* 
   * The actual "meat" of the doxygen parser. Calls the correct addCommand...()
   * function.
   */
  void addCommand(const std::string &commandString, const TokenList &tokList, DoxygenEntityList &doxyList);

  DoxygenEntityList parse(TokenListCIt endParsingIndex, const TokenList &tokList, bool root = false);

  /*
   * Fill static doxygenCommands and sectionIndicators containers
   */
  void fillTables();

  /** Processes comment when \htmlonly and \verbatim commands are encountered. */
  size_t processVerbatimText(size_t pos, const std::string &line);

  bool processEscapedChars(size_t &pos, const std::string &line);
  void processWordCommands(size_t &pos, const std::string &line);
  void processHtmlTags(size_t &pos, const std::string &line);
  void processHtmlEntities(