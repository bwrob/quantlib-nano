------------------------------------------------------
 * Strings.
 * ----------------------------------------------------------------------------- */

extern DOHString *DohNewStringEmpty(void);
extern DOHString *DohNewString(const DOHString_or_char *c);
extern DOHString *DohNewStringWithSize(const DOHString_or_char *c, int len);
extern DOHString *DohNewStringf(const DOHString_or_char *fmt, ...);

extern int DohStrcmp(const DOHString_or_char *s1, const DOHString_or_char *s2);
extern int DohStrncmp(const DOHString_or_char *s1, const DOHString_or_char *s2, int n);
extern char *DohStrstr(const DOHString_or_char *s1, const DOHString_or_char *s2);
extern char *DohStrchr(const DOHString_or_char *s1, int ch);

/* String replacement flags */

#define   DOH_REPLACE_ANY         0x01
#define   DOH_REPLACE_NOQUOTE     0x02
#define   DOH_REPLACE_NOCOMMENT   0x04
#define   DOH_REPLACE_ID          0x08
#define   DOH_REPLACE_FIRST       0x10
#define   DOH_REPLACE_ID_BEGIN    0x20
#define   DOH_REPLACE_ID_END      0x40
#define   DOH_REPLACE_NUMBER_END  0x80

#define Replaceall(s,t,r)  DohReplace(s,t,r,DOH_REPLACE_ANY)
#define Replaceid(s,t,r)   DohReplace(s,t,r,DOH_REPLACE_ID)

/* -----------------------------------------------------------------------------
 * Files
 * ----------------------------------------------------------------------------- */

extern DOHFile *DohNewFile(DOHString *filename, const char *mode, DOHList *outfiles);
extern DOHFile *DohNewFileFromFile(FILE *f);
extern DOHFile *DohNewFileFromFd(int fd);
extern void DohFileErrorDisplay(DOHString * filename);
extern int DohCopyto(DOHFile * input, DOHFile * output);
extern void DohCloseAllOpenFiles(void);


/* -----------------------------------------------------------------------------
 * List
 * ----------------------------------------------------------------------------- */

extern DOHList *DohNewList(void);
extern void DohSortList(DOH *lo, int (*cmp) (const DOH *, const DOH *));

/* -----------------------------------------------------------------------------
 * Hash
 * ----------------------------------------------------------------------------- */

extern DOHHash *DohNewHash(void);

/* -----------------------------------------------------------------------------
 * Void
 * ----------------------------------------------------------------------------- */

extern DOHVoid *DohNewVoid(void *ptr, void (*del) (void *));
extern DOHList *DohSplit(DOHFile * input, char ch, int nsplits);
extern DOHList *DohSplitLines(DOHFile * input);
extern DOH *DohNone;

/* Helper union for converting between function and object pointers. */
typedef union DohFuncPtr {
  void* p;
  DOH *(*func)(DOH *);
} DohFuncPtr_t;

extern void DohMemoryDebug(void);

#ifndef DOH_LONG_NAMES
/* Macros to invoke the above functions.  Includes the location of
   the caller to simplify debugging if something goes wrong */

#define Delete             DohDelete
#define Copy               DohCopy
#define Clear              DohClear
#define Str                DohStr
#define Dump               DohDump
#define Getattr            DohGetattr
#define Setattr            DohSetattr
#define Delattr            DohDelattr
#define Checkattr          DohCheckattr
#define Hashval            DohHashval
#define Getitem            DohGetitem
#define Setitem            DohSetitem
#define Delitem            DohDelitem
#define Insert             DohInsertitem
#define Delslice           DohDelslice
#define Append(s,x)        DohInsertitem(s,DOH_END,x)
#define Push(s,x)          DohInsertitem(s,DOH_BEGIN,x)
#define Len                DohLen
#define Data               DohData
#define Char(X)            ((char *) Data(X))
#define Cmp                DohCmp
#define Equal              DohEqual
#define Setline            DohSetline
#define Getline            DohGetline
#define Setfile            DohSetfile
#define Getfile            DohGetfile
#define Write              DohWrite
#define Read               DohRead
#define Seek               DohSeek
#d