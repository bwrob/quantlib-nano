g_or_char *name, const DOHObj_or_char * value);
extern int DohDelattr(DOH *obj, const DOHString_or_char *name);
extern int DohCheckattr(DOH *obj, const DOHString_or_char *name, const DOHString_or_char *value);
extern DOH *DohKeys(DOH *obj);
extern DOH *DohSortedKeys(DOH *obj, int (*cmp) (const DOH *, const DOH *));
extern int DohGetInt(DOH *obj, const DOHString_or_char *name);
extern void DohSetInt(DOH *obj, const DOHString_or_char *name, int);
extern double DohGetDouble(DOH *obj, const DOHString_or_char *name);
extern void DohSetDouble(DOH *obj, const DOHString_or_char *name, double);
extern char *DohGetChar(DOH *obj, const DOHString_or_char *name);
extern void DohSetChar(DOH *obj, const DOH *name, char *value);
extern void *DohGetFlagAttr(DOH *obj, const DOHString_or_char *name);
extern int DohGetFlag(DOH *obj, const DOHString_or_char *name);
extern void DohSetFlagAttr(DOH *obj, const DOHString_or_char *name, const DOHString_or_char *attr);
extern void DohSetFlag(DOH *obj, const DOHString_or_char *name);
extern void *DohGetVoid(DOH *obj, const DOHString_or_char *name);
extern void DohSetVoid(DOH *obj, const DOHString_or_char *name, void *value);

/* Sequence methods */

extern DOH *DohGetitem(DOH *obj, int index);
extern int DohSetitem(DOH *obj, int index, const DOHObj_or_char * value);
extern int DohDelitem(DOH *obj, int index);
extern int DohInsertitem(DOH *obj, int index, const DOHObj_or_char * value);
extern int DohDelslice(DOH *obj, int sindex, int eindex);

/* File methods */

extern int DohWrite(DOHFile * obj, const void *buffer, int length);
extern int DohRead(DOHFile * obj, void *buffer, int length);
extern int DohSeek(DOHFile * obj, long offset, int whence);
extern long DohTell(DOHFile * obj);
extern int DohGetc(DOHFile * obj);
extern int DohPutc(int ch, DOHFile * obj);
extern int DohUngetc(int ch, DOHFile * obj);



/* Iterators */
extern DohIterator DohFirst(DOH *obj);
extern DohIterator DohNext(DohIterator x);

/* Positional */

extern int DohGetline(const DOH *obj);
extern void DohSetline(DOH *obj, int line);
extern DOH *DohGetfile(const DOH *obj);
extern void DohSetfile(DOH *obj, DOH *file);

  /* String Methods */

extern int DohReplace(DOHString * src, const DOHString_or_char *token, const DOHString_or_char *rep, int flags);
extern void DohChop(DOHString * src);

/* Meta-variables */
extern DOH *DohGetmeta(DOH *, const DOH *);
extern int DohSetmeta(DOH *, const DOH *, const DOH *value);
extern int DohDelmeta(DOH *, const DOH *);

  /* Utility functions */

extern void DohEncoding(const char *name, DOH *(*fn) (DOH *s));
extern int DohPrintf(DOHFile * obj, const char *format, ...);
extern int DohvPrintf(DOHFile * obj, const char *format, va_list ap);
extern int DohPrintv(DOHFile * obj, ...);
extern DOH *DohReadline(DOHFile * in);

  /* Miscellaneous */

extern int DohIsMapping(const DOH *obj);
extern int DohIsSequence(const DOH *obj);
extern int DohIsString(const DOH *obj);
extern int DohIsFile(const DOH *obj);

extern void DohSetMaxHashExpand(int count);
extern int DohGetMaxHashExpand(void);
extern void DohSetmark(DOH *obj, int x);
extern int DohGetmark(DOH *obj);

/* Set the function for DohExit() to call instead of exit().
 *
 * The registered function can perform clean up, etc.  It should simply
 * return when done and then exit() will get called.  Bear in mind that
 * the handler function can be called after malloc() has failed, so it's
 * a good idea for it to avoid allocating additional memory.
 *
 * The registered handler function is unregistered by DohExit() before calling
 * it to avoid the potential for infinite loops.
 *
 * Note: This is sort of like C's atexit(), only for DohExit().  However
 * only one function can be registered (setting a new function overrides the
 * previous one) and the registered function is passed the exit status so can
 * vary its actions based on that.
 */
extern void DohSetExitHandler(void (*new_handler)(int));
extern void DohExit(int status);

/* -----------------------