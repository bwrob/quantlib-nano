s(ParmList *p);

/* --- Parse tree support --- */

#include "swigtree.h"

/* -- Wrapper function Object */

#include "swigwrap.h"

/* --- Naming functions --- */

  extern void Swig_name_register(const_String_or_char_ptr method, const_String_or_char_ptr format);
  extern void Swig_name_unregister(const_String_or_char_ptr method);
  extern String *Swig_name_type(const_String_or_char_ptr tname);
  extern String *Swig_name_mangle_string(const String *s);
  extern String *Swig_name_mangle_type(const SwigType *s);
  extern String *Swig_name_wrapper(const_String_or_char_ptr fname);
  extern String *Swig_name_member(const_String_or_char_ptr nspace, const_String_or_char_ptr classname, const_String_or_char_ptr membername);
  extern String *Swig_name_get(const_String_or_char_ptr nspace, const_String_or_char_ptr vname);
  extern String *Swig_name_set(const_String_or_char_ptr nspace, const_String_or_char_ptr vname);
  extern String *Swig_name_construct(const_String_or_char_ptr nspace, const_String_or_char_ptr classname);
  extern String *Swig_name_copyconstructor(const_String_or_char_ptr nspace, const_String_or_char_ptr classname);
  extern String *Swig_name_destroy(const_String_or_char_ptr nspace, const_String_or_char_ptr classname);
  extern String *Swig_name_disown(const_String_or_char_ptr nspace, const_String_or_char_ptr classname);

  extern void Swig_naming_init(void);
  extern void Swig_name_namewarn_add(String *prefix, String *name, SwigType *decl, Hash *namewrn);
  extern void Swig_name_rename_add(String *prefix, String *name, SwigType *decl, Hash *namewrn, ParmList *declaratorparms);
  extern void Swig_name_inherit(String *base, String *derived);
  extern List *Swig_make_inherit_list(String *clsname, List *names, String *Namespaceprefix);
  extern void Swig_inherit_base_symbols(List *bases);
  extern int Swig_need_protected(Node *n);
  extern int Swig_need_redefined_warn(Node *a, Node *b, int InClass);

  extern String *Swig_name_make(Node *n, String *prefix, const_String_or_char_ptr cname, SwigType *decl, String *oldname);
  extern String *Swig_name_warning(Node *n, String *prefix, String *name, SwigType *decl);
  extern String *Swig_name_str(Node *n);
  extern String *Swig_name_decl(Node *n);
  extern String *Swig_name_fulldecl(Node *n);

/* --- parameterized rename functions --- */

  extern void Swig_name_object_set(Hash *namehash, String *name, SwigType *decl, DOH *object);
  extern DOH *Swig_name_object_get(Hash *namehash, String *prefix, String *name, SwigType *decl);
  extern void Swig_name_object_inherit(Hash *namehash, String *base, String *derived);
  extern void Swig_features_get(Hash *features, String *prefix, String *name, SwigType *decl, Node *n);
  extern void Swig_feature_set(Hash *features, const_String_or_char_ptr name, SwigType *decl, const_String_or_char_ptr featurename, const_String_or_char_ptr value, Hash *featureattribs);

/* --- Misc --- */
  extern char *Swig_copy_string(const char *c);
  extern void Swig_set_fakeversion(const char *version);
  extern const char *Swig_package_version(void);
  extern String *Swig_package_version_hex(void);
  extern void Swig_obligatory_macros(String *f_runtime, const char *language);
  extern void Swig_banner(File *f);
  extern void Swig_banner_target_lang(File *f, const_String_or_char_ptr commentchar);
  extern String *Swig_strip_c_comments(const String *s);
  extern String *Swig_new_subdirectory(String *basedirectory, String *subdirectory);
  extern void Swig_filename_correct(String *filename);
  extern String *Swig_filename_escape(String *filename);
  extern String *Swig_filename_escape_space(String *filename);
  extern void Swig_filename_unescape(String *filename);
  extern int Swig_storage_isextern(Node *n);
  extern int Swig_storage_isexternc(Node *n);
  extern int Swig_storage_isstatic_custom(Node *n, const_String_or_char_ptr storage);
  extern int Swig_storage_isstatic(Node *n);
  extern String *Swig_string_escape(String *s);
  extern void Swig_scopename_split(co