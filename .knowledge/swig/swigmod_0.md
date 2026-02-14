/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3 
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * swigmod.h
 *
 * Main header file for SWIG modules.
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_SWIGMOD_H
#define SWIG_SWIGMOD_H

#include "swig.h"
#include "preprocessor.h"
#include "swigwarn.h"

#define NOT_VIRTUAL     0
#define PLAIN_VIRTUAL   1
#define PURE_VIRTUAL    2

extern String *input_file;
extern int line_number;
extern int start_line;
extern int CPlusPlus;		// C++ mode
extern int Extend;		// Extend mode
extern int Verbose;
extern int IsVirtual;
extern int ImportMode;
extern int NoExcept;		// -no_except option
extern int Abstract;		// abstract base class
extern int SmartPointer;	// smart pointer methods being emitted

/* Overload "argc" and "argv" */
extern String *argv_template_string;
extern String *argc_template_string;

/* Miscellaneous stuff */

#define  tab2   "  "
#define  tab4   "    "
#define  tab8   "        "

class Dispatcher {
public:

  Dispatcher ():cplus_mode(PUBLIC) {
  }
  virtual ~ Dispatcher () {
  }

  virtual int emit_one(Node *n);
  virtual int emit_children(Node *n);
  virtual int defaultHandler(Node *n);

  /* Top of the parse tree */
  virtual int top(Node *n) = 0;

  /* SWIG directives */

  virtual int applyDirective(Node *n);
  virtual int clearDirective(Node *n);
  virtual int constantDirective(Node *n);
  virtual int extendDirective(Node *n);
  virtual int fragmentDirective(Node *n);
  virtual int importDirective(Node *n);
  virtual int includeDirective(Node *n);
  virtual int insertDirective(Node *n);
  virtual int moduleDirective(Node *n);
  virtual int nativeDirective(Node *n);
  virtual int pragmaDirective(Node *n);
  virtual int typemapDirective(Node *n);
  virtual int typemapitemDirective(Node *n);
  virtual int typemapcopyDirective(Node *n);
  virtual int typesDirective(Node *n);

  /* C/C++ parsing */

  virtual int cDeclaration(Node *n);
  virtual int externDeclaration(Node *n);
  virtual int enumDeclaration(Node *n);
  virtual int enumvalueDeclaration(Node *n);
  virtual int enumforwardDeclaration(Node *n);
  virtual int classDeclaration(Node *n);
  virtual int classforwardDeclaration(Node *n);
  virtual int constructorDeclaration(Node *n);
  virtual int destructorDeclaration(Node *n);
  virtual int accessDeclaration(Node *n);
  virtual int usingDeclaration(Node *n);
  virtual int namespaceDeclaration(Node *n);
  virtual int templateDeclaration(Node *n);
  virtual int lambdaDeclaration(Node *n);

  enum AccessMode { PUBLIC, PRIVATE, PROTECTED };

protected:
  AccessMode cplus_mode;
  AccessMode accessModeFromString(String *access);
  int abstractClassTest(Node *n);	/* Is class really abstract? */
};

/* ----------------------------------------------------------------------------
 * class language:
 *
 * This class defines the functions that need to be supported by the
 * scripting language being used.    The translator calls these virtual
 * functions to output different types of code for different languages.
 * ------------------------------------------------------------------------- */

class Language:public Dispatcher {
public:
  Language();
  virtual ~Language();
  virtual int emit_one(Node *n);

  String *directorClassName(Node *n);

  /* Parse command line options */

  virtual void main(int argc, char *argv[]);

  /* Top of the parse tree */

  virtual int top(Node *n);

  /* SWIG directives */


  virtual int applyDirective(Node *n);
  virtual int clearDirective(Node *n);
  virtual int constantDirective(Node *n);
