rgs_init(int , char **);
void args_add(ARGS *args, const char *s);
void args_add_prefix(ARGS *args, const char *s);
void args_pop(ARGS *args, int n);
void args_strip(ARGS *args, const char *prefix);
void args_remove_first(ARGS *args);

extern int ccache_verbose;

#if HAVE_COMPAR_FN_T
#define COMPAR_FN_T __compar_fn_t
#else
typedef int (*COMPAR_FN_T)(const void *, const void *);
#endif

/* work with silly DOS binary open */
#ifndef O_BINARY
#define O_BINARY 0
#endif

/* mkstemp() on some versions of cygwin don't handle binary files, so
   override */
/* Seems okay in Cygwin 1.7.0
#ifdef __CYGWIN__
#undef HAVE_MKSTEMP
#endif
*/