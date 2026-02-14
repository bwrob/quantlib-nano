# ifndef DOH_NO_POISON_MALLOC_FREE
/* This works around bison's template checking if malloc and free are defined,
 * which triggers GCC's poison checks.
 */

#  pragma GCC poison malloc free

# endif

# pragma GCC poison realloc calloc
/* Use Exit() instead (which will remove output files on error). */

# pragma GCC poison abort exit
#endif

#endif				/* SWIG_DOH_H */