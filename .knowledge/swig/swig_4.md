nst String *s, String **prefix, String **last);
  extern String *Swig_scopename_prefix(const String *s);
  extern String *Swig_scopename_last(const String *s);
  extern String *Swig_scopename_first(const String *s);
  extern String *Swig_scopename_suffix(const String *s);
  extern List *Swig_scopename_tolist(const String *s);
  extern int Swig_scopename_check(const String *s);
  extern int Swig_scopename_isvalid(const String *s);
  extern String *Swig_string_lower(String *s);
  extern String *Swig_string_upper(String *s);
  extern String *Swig_string_title(String *s);
  extern void Swig_offset_string(String *s, int number);
  extern String *Swig_pcre_version(void);
  extern void Swig_init(void);

  extern int Swig_value_wrapper_mode(int mode);
  extern int Swig_is_generated_overload(Node *n);
  extern Node *Swig_item_in_list(List *list, const DOH *item);

  typedef enum { EMF_STANDARD, EMF_MICROSOFT } ErrorMessageFormat;

  extern void Swig_warning(int num, const_String_or_char_ptr filename, int line, const char *fmt, ...);
  extern void Swig_error(const_String_or_char_ptr filename, int line, const char *fmt, ...);
  extern int Swig_error_count(void);
  extern void Swig_error_silent(int s);
  extern void Swig_warnfilter(const_String_or_char_ptr wlist, int val);
  extern void Swig_warnall(void);
  extern int Swig_warn_count(void);
  extern void Swig_error_msg_format(ErrorMessageFormat format);
  extern void Swig_diagnostic(const_String_or_char_ptr filename, int line, const char *fmt, ...);
  extern String *Swig_stringify_with_location(DOH *object);

/* --- C Wrappers --- */
  extern void Swig_cresult_name_set(const char *new_name);
  extern const char *Swig_cresult_name(void);
  extern String *Swig_cparm_name(Parm *p, int i);
  extern String *Swig_wrapped_var_type(SwigType *t, int varcref);
  extern int Swig_cargs(Wrapper *w, ParmList *l);
  extern String *Swig_cresult(SwigType *t, const_String_or_char_ptr name, const_String_or_char_ptr decl);

  extern String *Swig_cfunction_call(const_String_or_char_ptr name, ParmList *parms);
  extern String *Swig_cconstructor_call(const_String_or_char_ptr name);
  extern String *Swig_cppconstructor_call(const_String_or_char_ptr name, ParmList *parms);
  extern String *Swig_unref_call(Node *n);
  extern String *Swig_ref_call(Node *n, const String *lname);
  extern String *Swig_cdestructor_call(Node *n);
  extern String *Swig_cppdestructor_call(Node *n);
  extern String *Swig_cmemberset_call(const_String_or_char_ptr name, SwigType *type, String *self, int varcref);
  extern String *Swig_cmemberget_call(const_String_or_char_ptr name, SwigType *t, String *self, int varcref);

  extern int Swig_add_extension_code(Node *n, const String *function_name, ParmList *parms, SwigType *return_type, const String *code, int cplusplus, const String *self);
  extern void Swig_replace_special_variables(Node *n, Node *parentnode, String *code);

/* --- Transformations --- */

  extern int Swig_MethodToFunction(Node *n, const_String_or_char_ptr nspace, String *classname, int flags, SwigType *director_type, int is_director);
  extern int Swig_ConstructorToFunction(Node *n, const_String_or_char_ptr nspace, String *classname, String *none_comparison, String *director_ctor, int cplus, int flags, String *directorname);
  extern int Swig_DestructorToFunction(Node *n, const_String_or_char_ptr nspace, String *classname, int cplus, int flags);
  extern int Swig_MembersetToFunction(Node *n, String *classname, int flags);
  extern int Swig_MembergetToFunction(Node *n, String *classname, int flags);
  extern int Swig_VargetToFunction(Node *n, int flags);
  extern int Swig_VarsetToFunction(Node *n, int flags);

#define  CWRAP_EXTEND                 0x01
#define  CWRAP_SMART_POINTER          0x02
#define  CWRAP_NATURAL_VAR            0x04
#define  CWRAP_DIRECTOR_ONE_CALL      0x08
#define  CWRAP_DIRECTOR_TWO_CALLS     0x10
#define  CWRAP_ALL_PROTECTED_ACCESS   0x20
#define  CWRAP_SMART_POINTER_OVERLOAD 0x40

/* --- Director 