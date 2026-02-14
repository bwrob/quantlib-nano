/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * doxyparser.h
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_DOXYPARSER_H
#define SWIG_DOXYPARSER_H
#include <string>
#include <list>
#include <map>
#include <vector>
#include <set>

#include "swig.h"

#include "doxyentity.h"

// Utility function to return the base part of a command that may
// include options, e.g. param[in] -> param
std::string getBaseCommand(const std::string &cmd);


class DoxygenParser {
private:

  enum DoxyCommandEnum {
    NONE = -1,
    SIMPLECOMMAND,
    COMMANDWORD,
    COMMANDLINE,
    COMMANDPARAGRAPH,
    COMMANDENDCOMMAND,
    COMMANDWORDPARAGRAPH,
    COMMANDWORDLINE,
    COMMANDWORDOWORDWORD,
    COMMANDOWORD,
    COMMANDERRORTHROW,
    COMMANDUNIQUE,
    COMMAND_HTML,
    COMMAND_HTML_ENTITY,
    COMMAND_ALIAS,
    COMMAND_IGNORE,
    END_LINE,
    PARAGRAPH_END,
    PLAINSTRING,
    COMMAND
  };


  /** This class contains parts of Doxygen comment as a token. */
  class Token {
  public:
    DoxyCommandEnum m_tokenType;
    std::string m_tokenString; /* the data , such as param for @param */

    Token(DoxyCommandEnum tType, std::string tString) : m_tokenType(tType), m_tokenString(tString) {
    }
    
    std::string toString() const {
      switch (m_tokenType) {
      case END_LINE:
        return "{END OF LINE}";
      case PARAGRAPH_END:
        return "{END OF PARAGRAPH}";
      case PLAINSTRING:
        return "{PLAINSTRING :" + m_tokenString + "}";
      case COMMAND:
        return "{COMMAND : " + m_tokenString + "}";
      default:
        return "";
      }
    }
  };


  typedef std::vector<Token> TokenList;
  typedef TokenList::const_iterator TokenListCIt;
  typedef TokenList::iterator TokenListIt;

  TokenList m_tokenList;
  TokenListCIt m_tokenListIt;

  typedef std::map<std::string, DoxyCommandEnum> DoxyCommandsMap;
  typedef DoxyCommandsMap::iterator DoxyCommandsMapIt;

  /*
   * Map of Doxygen commands to determine if a string is a
   * command and how it needs to be parsed
   */
  static DoxyCommandsMap doxygenCommands;
  static std::set<std::string> doxygenSectionIndicators;

  bool m_isVerbatimText; // used to handle \htmlonly and \verbatim commands
  bool m_isInQuotedString;

  Node *m_node;
  std::string m_fileName;
  int m_fileLineNo;

  /*
   * Return the end command for a command appearing in "ignore" feature or empty
   * string if this is a simple command and not a block one.
   */
  std::string getIgnoreFeatureEndCommand(const std::string &theCommand) const;

  /*
   * Helper for getting the value of doxygen:ignore feature or its argument.
   */
  String *getIgnoreFeature(const std::string &theCommand, const char *argument = NULL) const;

  /*
   * Whether to print lots of debug info during parsing
   */
  bool noisy;

  /*
   *Changes a std::string to all lower case
   */
  std::string stringToLower(const std::string &stringToConvert);

  /* 
   * isSectionIndicator returns a boolean if the command is a section indicator
   * This is a helper method for finding the end of a paragraph
   * by Doxygen's terms
   */
  bool isSectionIndicator(const std::string &smallString);
  /*
   * Determines how a command should be handled (what group it belongs to
   * for parsing rules
   */
  DoxyCommandEnum commandBelongs(const std::string &theCommand);

  /*
   *prints the parse tree
   */
  void printTree(const std::list<DoxygenEntity> &rootList);

  /**
   * Returns true if the next token is end of line token. This is impo