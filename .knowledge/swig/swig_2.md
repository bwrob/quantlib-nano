type(const SwigType *subtype, const SwigType *basetype);
  extern void SwigType_scope_alias(String *aliasname, Typetab *t);
  extern void SwigType_using_scope(Typetab *t);
  extern void SwigType_new_scope(const_String_or_char_ptr name);
  extern void SwigType_inherit_scope(Typetab *scope);
  extern Typetab *SwigType_pop_scope(void);
  extern Typetab *SwigType_set_scope(Typetab *h);
  extern void SwigType_print_scope(void);
  extern SwigType *SwigType_typedef_resolve(const SwigType *t);
  extern SwigType *SwigType_typedef_resolve_all(const SwigType *t);
  extern SwigType *SwigType_typedef_qualified(const SwigType *t);
  extern int SwigType_istypedef(const SwigType *t);
  extern int SwigType_isclass(const SwigType *t);
  extern void SwigType_attach_symtab(Symtab *syms);
  extern void SwigType_remember(const SwigType *t);
  extern void SwigType_remember_clientdata(const SwigType *t, const_String_or_char_ptr clientdata);
  extern void SwigType_remember_mangleddata(String *mangled, const_String_or_char_ptr clientdata);
  extern void (*SwigType_remember_trace(void (*tf) (const SwigType *, String *, String *))) (const SwigType *, String *, String *);
  extern void SwigType_emit_type_table(File *f_headers, File *f_table);
  extern int SwigType_type(const SwigType *t);

/* --- Symbol table module --- */

  extern void Swig_symbol_print_tables(Symtab *symtab);
  extern void Swig_symbol_print_tables_summary(void);
  extern void Swig_symbol_print_symbols(void);
  extern void Swig_symbol_print_csymbols(void);
  extern void Swig_symbol_init(void);
  extern void Swig_symbol_setscopename(const_String_or_char_ptr name);
  extern String *Swig_symbol_getscopename(void);
  extern String *Swig_symbol_qualifiedscopename(Symtab *symtab);
  extern String *Swig_symbol_qualified_language_scopename(Symtab *symtab);
  extern Symtab *Swig_symbol_newscope(void);
  extern Symtab *Swig_symbol_setscope(Symtab *);
  extern Symtab *Swig_symbol_getscope(const_String_or_char_ptr symname);
  extern Symtab *Swig_symbol_global_scope(void);
  extern Symtab *Swig_symbol_current(void);
  extern Symtab *Swig_symbol_popscope(void);
  extern Node *Swig_symbol_add(const_String_or_char_ptr symname, Node *n);
  extern void Swig_symbol_conflict_warn(Node *n, Node *c, const String *symname, int inclass);
  extern void Swig_symbol_cadd(const_String_or_char_ptr symname, Node *n);
  extern Node *Swig_symbol_clookup(const_String_or_char_ptr symname, Symtab *tab);
  extern Node *Swig_symbol_clookup_check(const_String_or_char_ptr symname, Symtab *tab, Node *(*checkfunc) (Node *));
  extern Node *Swig_symbol_clookup_no_inherit(const_String_or_char_ptr name, Symtab *n);
  extern Symtab *Swig_symbol_cscope(const_String_or_char_ptr symname, Symtab *tab);
  extern Node *Swig_symbol_clookup_local(const_String_or_char_ptr symname, Symtab *tab);
  extern Node *Swig_symbol_clookup_local_check(const_String_or_char_ptr symname, Symtab *tab, Node *(*checkfunc) (Node *));
  extern String *Swig_symbol_qualified(Node *n);
  extern Node *Swig_symbol_isoverloaded(Node *n);
  extern void Swig_symbol_remove(Node *n);
  extern void Swig_symbol_fix_overname(Node *n);
  extern void Swig_symbol_alias(const_String_or_char_ptr aliasname, Symtab *tab);
  extern void Swig_symbol_inherit(Symtab *tab);
  extern SwigType *Swig_symbol_type_qualify(const SwigType *ty, Symtab *tab);
  extern String *Swig_symbol_string_qualify(String *s, Symtab *tab);
  extern SwigType *Swig_symbol_typedef_reduce(const SwigType *ty, Symtab *tab);

  extern ParmList *Swig_symbol_template_defargs(Parm *parms, Parm *targs, Symtab *tscope, Symtab *tsdecl);
  extern SwigType *Swig_symbol_template_deftype(const SwigType *type, Symtab *tscope);
  extern SwigType *Swig_symbol_template_param_eval(const SwigType *p, Symtab *symtab);
  extern int Swig_symbol_isvalid(const String *s);

/* --- Parameters and Parameter Lists --- */

#include "swigparm.h"

extern String    *ParmList_errorstr(ParmList *);
extern int        ParmList_is_compactdefarg