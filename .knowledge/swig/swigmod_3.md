ultiple_inheritance;

  /* Used to translate Doxygen comments to target documentation format */
  class DoxygenTranslator *doxygenTranslator;

private:
  void unrollOneVirtualMethod(String *classname, Node *n, Node *parent, List *vm, int &virtual_destructor, int protectedbase);

  Hash *symtabs; /* symbol tables */
  int overloading;
  int multiinput;
  int cplus_runtime;
  static Language *this_;
};

extern "C" {
  typedef Language *(*ModuleFactory) (void);
}

enum Status {Disabled, Deprecated, Experimental, Supported};

struct TargetLanguageModule {
  const char *name;
  ModuleFactory fac;
  const char *help;
  Status status;
};

int SWIG_main(int argc, char *argv[], const TargetLanguageModule *tlm);
void emit_parameter_variables(ParmList *l, Wrapper *f);
void emit_return_variable(Node *n, SwigType *rt, Wrapper *f);
void SWIG_config_file(const_String_or_char_ptr );
const String *SWIG_output_directory();
void SWIG_config_cppext(const char *ext);
void Swig_print_xml(Node *obj, String *filename);

/* get the list of generated files */
List *SWIG_output_files();

void SWIG_library_directory(const char *);
int emit_num_arguments(ParmList *);
int emit_num_required(ParmList *);
int emit_isvarargs(ParmList *p);
bool emit_isvarargs_function(Node *n);
void emit_attach_parmmaps(ParmList *, Wrapper *f);
void emit_mark_varargs(ParmList *l);
String *emit_action(Node *n);
int emit_action_code(Node *n, String *wrappercode, String *action);
void Swig_overload_check(Node *n);
String *Swig_overload_dispatch(Node *n, const_String_or_char_ptr fmt, int *maxargs, bool *check_emitted, const_String_or_char_ptr fmt_fastdispatch = 0);
String *Swig_overload_dispatch_cast(Node *n, const_String_or_char_ptr fmt, int *maxargs, bool *check_emitted);
List *Swig_overload_rank(Node *n, bool script_lang_wrapping);
SwigType *cplus_value_type(SwigType *t);

int Swig_directors_enabled();
/* directors.cxx start */
String *Swig_csuperclass_call(String *base, String *method, ParmList *l);
String *Swig_class_declaration(Node *n, String *name);
String *Swig_class_name(Node *n);
String *Swig_method_call(const_String_or_char_ptr name, ParmList *parms);
String *Swig_method_decl(SwigType *return_base_type, SwigType *decl, const_String_or_char_ptr id, List *args, int default_args);
String *Swig_director_declaration(Node *n);
void Swig_director_emit_dynamic_cast(Node *n, Wrapper *f);
void Swig_director_parms_fixup(ParmList *parms);
bool Swig_director_can_unwrap(Node *n);
/* directors.cxx end */

/* Utilities */

int is_public(Node *n);
int is_private(Node *n);
int is_protected(Node *n);
int is_member_director(Node *parentnode, Node *member);
int is_member_director(Node *member);
int is_non_virtual_protected_access(Node *n); /* Check if the non-virtual protected members are required (for directors) */

void Wrapper_virtual_elimination_mode_set(int);
void Wrapper_fast_dispatch_mode_set(int);
void Wrapper_cast_dispatch_mode_set(int);
void Wrapper_naturalvar_mode_set(int);

void clean_overloaded(Node *n);

extern "C" {
  const char *Swig_to_string(DOH *object, int count = -1);
  const char *Swig_to_string_with_location(DOH *object, int count = -1);
  void Swig_print(DOH *object, int count = -1);
  void Swig_print_with_location(DOH *object, int count = -1);
}

void Swig_default_allocators(Node *n);
void Swig_process_types(Node *n);

/* Contracts */
void Swig_contracts(Node *n);
void Swig_contract_mode_set(int flag);
int Swig_contract_mode_get();

/* Nested classes */
void Swig_nested_process_classes(Node *n);
void Swig_nested_name_unnamed_c_structs(Node *n);

/* Interface feature */
void Swig_interface_feature_enable();
void Swig_interface_propagate_methods(Node *n);

/* Miscellaneous */
template <class T> class save_value {
  T _value;
  T& _value_ptr;
  save_value(const save_value&);
  save_value& operator=(const save_value&);

public:
  save_value(T& value) : _value(value), _value_ptr(value) {}
  save_value(T& value, T new_val) : _value(value), _value_ptr(value) { value = new_