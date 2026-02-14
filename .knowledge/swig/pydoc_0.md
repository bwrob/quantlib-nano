/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * pydoc.h
 *
 * Module to return documentation for nodes formatted for PyDoc
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_PYDOC_H
#define SWIG_PYDOC_H

#include <list>
#include <string>
#include "swig.h"
#include "doxyentity.h"
#include "doxytranslator.h"

#define DOC_STRING_LENGTH         64 // characters per line allowed
#define DOC_PARAM_STRING_LENGTH   30 // characters reserved for param name / type

class PyDocConverter : public DoxygenTranslator {
public:
  PyDocConverter(int flags = 0);
  String *makeDocumentation(Node *node);

protected:

  size_t m_tableLineLen;
  bool m_prevRowIsTH;
  std::string m_url;

  /*
   * Translate every entity in a tree, also manages sections
   * display. Prints title for every group of tags that have
   * a section title associated with them
   */
  std::string translateSubtree(DoxygenEntity &doxygenEntity);

  /*
   * Translate one entity with the appropriate handler, according
   * to the tagHandlers
   */
  void translateEntity(DoxygenEntity &doxyEntity, std::string &translatedComment);

  /*
   * Typedef for the function that handles one tag
   * arg - some string argument to easily pass it through lookup table
   */
  typedef void (PyDocConverter::*tagHandler) (DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Wrap the command data with the some string
   * arg - string to wrap with, like '_' or '*'
   */
  void handleTagWrap(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Just prints new line
   */
  void handleNewLine(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Print the name of tag to the output, used for escape-commands
   */
  void handleTagChar(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Format the contents of the \exception tag or its synonyms.
   */
  void handleTagException(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Print only the content and strip original tag
   */
  void handleParagraph(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg = std::string());

  /*
   * Handle Doxygen verbatim tag
   */
  void handleVerbatimBlock(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg = std::string());

  /*
   * Handle one of the Doxygen formula-related tags.
   */
  void handleMath(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Handle a code snippet.
   */
  void handleCode(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Print only data part of code
   */
  void handlePlainString(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /**
   * Copies verbatim args of the tag to output, used for commands like \f$, ...
   */
  void handleTagVerbatim(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Print the if-elseif-else-endif section
   */
  void handleTagIf(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Prints the specified message, than the contents of the tag
   * arg - message
   */
  void handleTagMessage(DoxygenEntity &tag, std::string &translatedComment, const std::string &arg);

  /*
   * Insert 'Title: ...'
   */
  void handleTagPar(DoxygenEntity &tag, std::string &translatedComment, c