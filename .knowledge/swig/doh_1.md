      DOH_NAMESPACE(IsFile)
#define DohNewString       DOH_NAMESPACE(NewString)
#define DohNewStringEmpty  DOH_NAMESPACE(NewStringEmpty)
#define DohNewStringWithSize  DOH_NAMESPACE(NewStringWithSize)
#define DohNewStringf      DOH_NAMESPACE(NewStringf)
#define DohStrcmp          DOH_NAMESPACE(Strcmp)
#define DohStrncmp         DOH_NAMESPACE(Strncmp)
#define DohStrstr          DOH_NAMESPACE(Strstr)
#define DohStrchr          DOH_NAMESPACE(Strchr)
#define DohNewFile         DOH_NAMESPACE(NewFile)
#define DohNewFileFromFile DOH_NAMESPACE(NewFileFromFile)
#define DohNewFileFromFd   DOH_NAMESPACE(NewFileFromFd)
#define DohFileErrorDisplay   DOH_NAMESPACE(FileErrorDisplay)
#define DohCopyto          DOH_NAMESPACE(Copyto)
#define DohNewList         DOH_NAMESPACE(NewList)
#define DohNewHash         DOH_NAMESPACE(NewHash)
#define DohNewVoid         DOH_NAMESPACE(NewVoid)
#define DohSplit           DOH_NAMESPACE(Split)
#define DohSplitLines      DOH_NAMESPACE(SplitLines)
#define DohNone            DOH_NAMESPACE(None)
#define DohCall            DOH_NAMESPACE(Call)
#define DohObjMalloc       DOH_NAMESPACE(ObjMalloc)
#define DohObjFree         DOH_NAMESPACE(ObjFree)
#define DohMemoryDebug     DOH_NAMESPACE(MemoryDebug)
#define DohStringType      DOH_NAMESPACE(StringType)
#define DohListType        DOH_NAMESPACE(ListType)
#define DohHashType        DOH_NAMESPACE(HashType)
#define DohFileType        DOH_NAMESPACE(FileType)
#define DohVoidType        DOH_NAMESPACE(VoidType)
#define DohIterator        DOH_NAMESPACE(Iterator)
#define DohFirst           DOH_NAMESPACE(First)
#define DohNext            DOH_NAMESPACE(Next)
#define DohMalloc          DOH_NAMESPACE(Malloc)
#define DohRealloc         DOH_NAMESPACE(Realloc)
#define DohCalloc          DOH_NAMESPACE(Calloc)
#define DohFree            DOH_NAMESPACE(Free)
#define DohSetExitHandler  DOH_NAMESPACE(SetExitHandler)
#define DohExit            DOH_NAMESPACE(Exit)
#endif

#define DOH_MAJOR_VERSION 0
#define DOH_MINOR_VERSION 1

typedef void DOH;

/*
 * With dynamic typing, all DOH objects are technically of type 'void *'.
 * However, to clarify the reading of source code, the following symbolic
 * names are used.
 */

#define DOHString          DOH
#define DOHList            DOH
#define DOHHash            DOH
#define DOHFile            DOH
#define DOHVoid            DOH
#define DOHString_or_char  DOH
#define DOHObj_or_char     DOH

typedef const DOHString_or_char * const_String_or_char_ptr;
typedef const DOHString_or_char * DOHconst_String_or_char_ptr;

#define DOH_BEGIN          -1
#define DOH_END            -2
#define DOH_CUR            -3
#define DOH_CURRENT        -3

/* Iterator objects */

typedef struct {
  void *key;			/* Current key (if any)       */
  void *item;			/* Current item               */
  void *object;			/* Object being iterated over */
  void *_current;		/* Internal use */
  int _index;			/* Internal use */
} DohIterator;

/* Memory management */

/* Wrappers around malloc(), realloc() and calloc() which never return NULL. */
extern void *DohMalloc(size_t size);
extern void *DohRealloc(void *ptr, size_t size);
extern void *DohCalloc(size_t n, size_t size);

#ifndef DohFree
#define DohFree free
#endif

extern int DohCheck(const DOH *ptr);	/* Check if a DOH object */
extern void DohIntern(DOH *);	/* Intern an object      */

/* Basic object methods.  Common to most objects */

extern void DohDelete(DOH *obj);	/* Delete an object      */
extern DOH *DohCopy(const DOH *obj);
extern void DohClear(DOH *obj);
extern DOHString *DohStr(const DOH *obj);
extern void *DohData(const DOH *obj);
extern int DohDump(const DOH *obj, DOHFile * out);
extern int DohLen(const DOH *obj);
extern int DohHashval(const DOH *obj);
extern int DohCmp(const DOH *obj1, const DOH *obj2);
extern int DohEqual(const DOH *obj1, const DOH *obj2);
extern void DohIncref(DOH *obj);

/* Mapping methods */

extern DOH *DohGetattr(DOH *obj, const DOHString_or_char *name);
extern int DohSetattr(DOH *obj, const DOHStrin