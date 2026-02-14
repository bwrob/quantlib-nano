Helpers --- */
  extern Node *Swig_methodclass(Node *n);
  extern int Swig_directorclass(Node *n);
  extern Node *Swig_directormap(Node *n, String *type);

/* --- Legacy Typemap API (somewhat simplified, ha!) --- */

  extern void Swig_typemap_init(void);
  extern void Swig_typemap_register(const_String_or_char_ptr tmap_method, ParmList *pattern, const_String_or_char_ptr code, ParmList *locals, ParmList *kwargs);
  extern int Swig_typemap_copy(const_String_or_char_ptr tmap_method, ParmList *srcpattern, ParmList *pattern);
  extern void Swig_typemap_clear(const_String_or_char_ptr tmap_method, ParmList *pattern);
  extern int Swig_typemap_apply(ParmList *srcpat, ParmList *destpat);
  extern void Swig_typemap_clear_apply(ParmList *pattern);
  extern void Swig_typemap_replace_embedded_typemap(String *s, Node *file_line_node);
  extern void Swig_typemap_debug(void);
  extern void Swig_typemap_search_debug_set(void);
  extern void Swig_typemap_used_debug_set(void);
  extern void Swig_typemap_register_debug_set(void);

  extern String *Swig_typemap_lookup(const_String_or_char_ptr tmap_method, Node *n, const_String_or_char_ptr lname, Wrapper *f);
  extern String *Swig_typemap_lookup_out(const_String_or_char_ptr tmap_method, Node *n, const_String_or_char_ptr lname, Wrapper *f, String *actioncode);

  extern void Swig_typemap_attach_parms(const_String_or_char_ptr tmap_method, ParmList *parms, Wrapper *f);

/* --- Code fragment support --- */

  extern void Swig_fragment_register(Node *fragment);
  extern void Swig_fragment_emit(String *name);
  extern void Swig_fragment_clear(String *section);

/* --- Extension support --- */

  extern Hash *Swig_extend_hash(void);
  extern void Swig_extend_merge(Node *cls, Node *am);
  extern void Swig_extend_append_previous(Node *cls, Node *am);
  extern void Swig_extend_unused_check(void);

/* hacks defined in C++ ! */
  extern int Swig_director_mode(void);
  extern int Swig_director_protected_mode(void);
  extern int Swig_all_protected_mode(void);
  extern void Wrapper_director_mode_set(int);
  extern void Wrapper_director_protected_mode_set(int);
  extern void Wrapper_all_protected_mode_set(int);
  extern void Language_replace_special_variables(String *method, String *tm, Parm *parm);
  extern void Swig_print(DOH *object, int count);
  extern void Swig_print_with_location(DOH *object, int count);

/* -- template init -- */
  extern void SwigType_template_init(void);


#ifdef __cplusplus
}
#endif
#endif