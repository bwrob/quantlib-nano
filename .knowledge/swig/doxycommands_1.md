onst int commandWordLinesSize = sizeof(commandWordLines) / sizeof(*commandWordLines);

const char *commandWordOWordOWords[] = {
  "category", "class", "protocol", "interface", "struct", "union"
};

const int commandWordOWordOWordsSize = sizeof(commandWordOWordOWords) / sizeof(*commandWordOWordOWords);

const char *commandOWords[] = {
  "dir", "file", "cond"
};

const int commandOWordsSize = sizeof(commandOWords) / sizeof(*commandOWords);

const char *commandErrorThrowings[] = {
  "annotatedclassstd::list", "classhierarchy", "define", "functionindex", "header",
  "headerfilestd::list", "inherit", "l", "postheader", "endcode", "enddot", "endmsc", "endhtmlonly",
  "endlatexonly", "endmanonly", "endlink", "endverbatim", "endxmlonly", "f]", "f}", "endif", "else",
  "endrtfonly"
};

const int commandErrorThrowingsSize = sizeof(commandErrorThrowings) / sizeof(*commandErrorThrowings);

const char *commandUniques[] = {
  "xrefitem", "arg", "ingroup", "par", "headerfile", "overload", "weakgroup", "ref", "subpage", "dotfile", "image", "addtogroup", "li",
  "if", "ifnot", "elseif", "else", "mscfile", "code", CMD_VERBATIM, "f{", "f[", "f$", "dot", "msc"
};

const int commandUniquesSize = sizeof(commandUniques) / sizeof(*commandUniques);

// These HTML commands are transformed when producing output in other formats.
// Other commands are left intact, but '<' and '> are replaced with entities in HTML
// output. So <varName> appears as &lt;varName&gt; in HTML output. The same
// behavior must be repeated by SWIG. See Doxygen doc for the list of commands.
// '<' is prepended to distinguish HTML tags from Doxygen commands.
const char *commandHtml[] = {
  "<a", "<b", "<blockquote", "<body", "<br", "<center", "<caption", "<code", "<dd", "<dfn",
  "<div", "<dl", "<dt", "<em", "<form", "<hr", "<h1", "<h2", "<h3", "<i", "<input", "<img",
  "<li", "<meta", "<multicol", "<ol", "<p", "<pre", "<small", "<span", "<strong",
  "<sub", "<sup", "<table", "<td", "<th", "<tr", "<tt", "<kbd", "<ul", "<var"
};

const int commandHtmlSize = sizeof(commandHtml) / sizeof(*commandHtml);

// Only entities which are translatable to plain text are used here. Others
// are copied unchanged to output.
const char *commandHtmlEntities[] = {
  "&copy",                  // (C)
  "&trade",                 // (TM)
  "&reg",                   // (R)
  "&lt",                    // less-than symbol
  "&gt",                    // greater-than symbol
  "&amp",                   // ampersand
  "&apos",                  // single quotation mark (straight)
  "&quot",                  // double quotation mark (straight)
  "&lsquo",                 // left single quotation mark
  "&rsquo",                 // right single quotation mark
  "&ldquo",                 // left double quotation mark
  "&rdquo",                 // right double quotation mark
  "&ndash",                 // n-dash (for numeric ranges, e.g. 2–8)
  "&mdash",                 // --
  "&nbsp",                  //
  "&times",                 // x
  "&minus",                 // -
  "&sdot",                  // .
  "&sim",                   // ~
  "&le",                    // <=
  "&ge",                    // >=
  "&larr",                  // <--
  "&rarr"                   // -->
};

const int commandHtmlEntitiesSize = sizeof(commandHtmlEntities) / sizeof(*commandHtmlEntities);

#endif