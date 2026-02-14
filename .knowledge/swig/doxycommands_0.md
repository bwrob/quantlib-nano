/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * doxycommands.h
 *
 * Part of the Doxygen comment translation module of SWIG.
 * ----------------------------------------------------------------------------- */

#ifndef DOXYGENCOMMANDS_H
#define DOXYGENCOMMANDS_H

// doxy commands are not processed inside this block
const char *CMD_HTML_ONLY = "htmlonly";
// doxy commands are not processed inside this block
const char *CMD_VERBATIM = "verbatim";
const char *CMD_CODE = "code";
const char *CMD_LATEX_1 = "f$";
const char *CMD_LATEX_2 = "f{";
const char *CMD_LATEX_3 = "f[";
const char *CMD_END_HTML_ONLY = "endhtmlonly";
const char *CMD_END_VERBATIM = "endverbatim";
const char *CMD_END_CODE = "endcode";
const char *CMD_END_LATEX_1 = "f$";
const char *CMD_END_LATEX_2 = "f}";
const char *CMD_END_LATEX_3 = "f]";

const char *sectionIndicators[] = {
  "attention", "author", "authors", "brief", "bug", "cond", "date",
  "deprecated", "details", "else", "elseif", "endcond", "endif",
  "exception", "if", "ifnot", "invariant", "note", "par", "param",
  "tparam", "post", "pre", "remarks", "remark", "result", "return",
  "returns", "retval", "sa", "see", "since", "test", "throw", "throws",
  "todo", "version", "warning", "xrefitem"
};

const int sectionIndicatorsSize = sizeof(sectionIndicators) / sizeof(*sectionIndicators);

/* All of the doxygen commands divided up by how they are parsed */
const char *simpleCommands[] = {
  // the first line are escaped chars, except \~, which is a language ID command.
  "n", "$", "@", "\\", "&", "~", "<", ">", "#", "%", "\"", ".", "::",
  // Member groups, which we currently ignore.
  "{", "}",
  "endcond",
  "callgraph", "callergraph", "showinitializer", "hideinitializer", "internal",
  "nosubgrouping", "public", "publicsection", "private", "privatesection",
  "protected", "protectedsection", "tableofcontents"
};

const int simpleCommandsSize = sizeof(simpleCommands) / sizeof(*simpleCommands);

const char *commandWords[] = {
  "a", "b", "c", "e", "em", "p", "def", "enum", "package", "relates",
  "namespace", "relatesalso", "anchor", "dontinclude", "include",
  "includelineno", "copydoc", "copybrief", "copydetails", "verbinclude",
  "htmlinclude", "extends", "implements", "memberof", "related", "relatedalso",
  "cite"
};

const int commandWordsSize = sizeof(commandWords) / sizeof(*commandWords);

const char *commandLines[] = {
  "addindex", "fn", "name", "line", "var", "skipline", "typedef", "skip",
  "until", "property"
};

const int commandLinesSize = sizeof(commandLines) / sizeof(*commandLines);

const char *commandParagraph[] = {
  "partofdescription", "result", "return", "returns", "remarks", "remark",
  "since", "test", "sa", "see", "pre", "post", "details", "invariant",
  "deprecated", "date", "note", "warning", "version", "todo", "bug",
  "attention", "brief", "author", "authors", "copyright", "short"
};

const int commandParagraphSize = sizeof(commandParagraph) / sizeof(*commandParagraph);

const char *commandEndCommands[] = {
  CMD_HTML_ONLY, "latexonly", "manonly", "xmlonly", "link", "rtfonly"
};

const int commandEndCommandsSize = sizeof(commandEndCommands) / sizeof(*commandEndCommands);

const char *commandWordParagraphs[] = {
  "param", "tparam", "throw", "throws", "retval", "exception", "example"
};

const int commandWordParagraphsSize = sizeof(commandWordParagraphs) / sizeof(*commandWordParagraphs);

const char *commandWordLines[] = {
  "page", "subsection", "subsubsection", "section", "paragraph", "defgroup",
  "snippet", "mainpage"
};

c