size_t &pos, const std::string &line);


  /** Processes comment outside \htmlonly and \verbatim commands. */
  size_t processNormalComment(size_t pos, const std::string &line);

  void tokenizeDoxygenComment(const std::string &doxygenComment, const std::string &fileName, int fileLine);
  void printList();
  void printListError(int warningType, const std::string &message);

  typedef std::vector<std::string> StringVector;
  typedef StringVector::const_iterator StringVectorCIt;

  StringVector split(const std::string &text, char separator);
  bool isStartOfDoxyCommentChar(char c);
  bool addDoxyCommand(DoxygenParser::TokenList &tokList, const std::string &cmd);

public:
  DoxygenParser(bool noisy = false);
  virtual ~DoxygenParser();
  DoxygenEntityList createTree(Node *node, String *documentation);
};

#endif