  virtual int extendDirective(Node *n);
  virtual int fragmentDirective(Node *n);
  virtual int importDirective(Node *n);
  virtual int includeDirective(Node *n);
  virtual int insertDirective(Node *n);
  virtual int moduleDirective(Node *n);
  virtual int nativeDirective(Node *n);
  virtual int pragmaDirective(Node *n);
  virtual int typemapDirective(Node *n);
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
  virtual int namespaceDeclaration(Node *n);
  virtual int usingDeclaration(Node *n);

  /* Function handlers */

  virtual int functionHandler(Node *n);
  virtual int globalfunctionHandler(Node *n);
  virtual int memberfunctionHandler(Node *n);
  virtual int staticmemberfunctionHandler(Node *n);
  virtual int callbackfunctionHandler(Node *n);

  /* Variable handlers */

  virtual int variableHandler(Node *n);
  virtual int globalvariableHandler(Node *n);
  virtual int membervariableHandler(Node *n);
  virtual int staticmembervariableHandler(Node *n);

  /* C++ handlers */

  virtual int memberconstantHandler(Node *n);
  virtual int constructorHandler(Node *n);
  virtual int copyconstructorHandler(Node *n);
  virtual int destructorHandler(Node *n);
  virtual int classHandler(Node *n);

  /* Miscellaneous */

  virtual int typedefHandler(Node *n);

  /* Low-level code generation */

  virtual int constantWrapper(Node *n);
  virtual int variableWrapper(Node *n);
  virtual int functionWrapper(Node *n);
  virtual int nativeWrapper(Node *n);

  /* C++ director class generation */
  virtual int classDirector(Node *n);
  virtual int classDirectorInit(Node *n);
  virtual int classDirectorEnd(Node *n);
  virtual int unrollVirtualMethods(Node *n, Node *parent, List *vm, int &virtual_destructor, int protectedbase = 0);
  virtual int classDirectorConstructor(Node *n);
  virtual int classDirectorDefaultConstructor(Node *n);
  virtual int classDirectorMethod(Node *n, Node *parent, String *super);
  virtual int classDirectorConstructors(Node *n);
  virtual int classDirectorDestructor(Node *n);
  virtual int classDirectorMethods(Node *n);
  virtual int classDirectorDisown(Node *n);

  /* Miscellaneous */
  virtual int validIdentifier(String *s);	/* valid identifier? */
  virtual int addSymbol(const String *s, const Node *n, const_String_or_char_ptr scope = "");	/* Add symbol        */
  virtual int addInterfaceSymbol(const String *interface_name, Node *n, const_String_or_char_ptr scope = "");
  virtual void dumpSymbols();
  virtual Node *symbolLookup(const String *s, const_String_or_char_ptr scope = ""); /* Symbol lookup */
  virtual Hash* symbolAddScope(const_String_or_char_ptr scope/*, Node *n = 0*/);
  virtual Hash* symbolScopeLookup(const_String_or_char_ptr scope);
  virtual Hash* symbolScopePseudoSymbolLookup(const_String_or_char_ptr scope);
  static Node *classLookup(const SwigType *s); /* Class lookup      */
  static Node *enumLookup(SwigType *s);	/* Enum lookup       */
  virtual int is_immutable(Node *n);	/* Is variable assignable? */
  virtual String *runtimeCode();	/* returns the language specific runtime code */
  virtual String *defaultExternalRuntimeFilename();	/* the default filename for the external runtime */
  virtual void replaceSpecialVariables(String *method, String *tm, Parm *parm); /* Language specific special variable substitutions for $typemap() */

  /* Runtime is C++ based, so extern "C" header section */
  void enable_cplus_runtime_mode();

  /* Returns the cplus_runtime mode */
  int cplus_runtime_mode();

  /* Flag for lan