guage to support directors */
  void directorLanguage(int val = 1);

  /* Allow director related code generation */
  void allow_directors(int val = 1);

  /* Allow director protected members related code generation */
  void allow_dirprot(int val = 1);

  /* Allow all protected members code generation (for directors) */
  void allow_allprotected(int val = 0);

  /* Returns the dirprot mode */
  int dirprot_mode() const;

  /* Check if the non public constructor is needed (for directors) */
  int need_nonpublic_ctor(Node *n);

  /* Check if the non public member is needed (for directors) */
  int need_nonpublic_member(Node *n);

  /* Set none comparison string */
  void setSubclassInstanceCheck(String *s);

  /* Set overload variable templates argc and argv */
  void setOverloadResolutionTemplates(String *argc, String *argv);

  /* Language instance is a singleton - get instance */
  static Language* instance();

protected:
  /* Allow multiple-input typemaps */
  void allow_multiple_input(int val = 1);

  /* Allow overloaded functions */
  void allow_overloading(int val = 1);

  /* Wrapping class query */
  int is_wrapping_class() const;

  /* Return the node for the current class */
  Node *getCurrentClass() const;

  /* Return C++ mode */
  int getCPlusMode() const;

  /* Return the namespace for the class/enum - the nspace feature */
  String *getNSpace() const;

  /* Return the real name of the current class */
  String *getClassName() const;

  /* Return the classes hash */
  Hash *getClassHash() const;

  /* Return the current class prefix */
  String *getClassPrefix() const;

  /* Return the current enum class prefix */
  String *getEnumClassPrefix() const;

  /* Fully qualified type name to use */
  String *getClassType() const;

  /* Return true if the current method is part of a smart-pointer */
  int is_smart_pointer() const;

  /* Return the name to use for the given parameter. */
  virtual String *makeParameterName(Node *n, Parm *p, int arg_num, bool setter = false) const;

  /* Some language modules require additional wrappers for virtual methods not declared in sub-classes */
  virtual bool extraDirectorProtectedCPPMethodsRequired() const;

public:
  enum NestedClassSupport {
    NCS_None, // Target language does not have an equivalent to nested classes
    NCS_Full, // Target language does have an equivalent to nested classes and is fully implemented
    NCS_Unknown // Target language may or may not have an equivalent to nested classes. If it does, it has not been implemented yet.
  };
  /* Does target language support nested classes? Default is NCS_Unknown. 
    If NCS_Unknown is returned, then the nested classes will be ignored unless 
    %feature "flatnested" is applied to them, in which case they will appear in global space.
    If the target language does not support the notion of class
    nesting, the language module should return NCS_None from this function, and 
    the nested classes will be moved to the global scope (like implicit global %feature "flatnested").
  */
  virtual NestedClassSupport nestedClassesSupport() const;

  /* Returns true if the target language supports key word arguments (kwargs) */
  virtual bool kwargsSupport() const;

protected:
  /* Identifies if a protected members that are generated when the allprotected option is used.
     This does not include protected virtual methods as they are turned on with the dirprot option. */
  bool isNonVirtualProtectedAccess(Node *n) const;

  /* Identify if a wrapped global or member variable n should use the naturalvar feature */
  int use_naturalvar_mode(Node *n) const;

  /* Director subclass comparison test */
  String *none_comparison;

  /* Director constructor "template" code */
  String *director_ctor_code;

  /* Director 'protected' constructor "template" code, disabled by
     default. Each language that needs it, has to define it. */
  String *director_prot_ctor_code;

  /* Director allows multiple inheritance */
  int director_m