efine Tell               DohTell
#define Printf             DohPrintf
#define Printv             DohPrintv
#define Getc               DohGetc
#define Putc               DohPutc
#define Ungetc             DohUngetc

/* #define StringPutc         DohStringPutc */
/* #define StringGetc         DohStringGetc */
/* #define StringUngetc       DohStringUngetc */
/* #define StringAppend       Append */
/* #define StringLen          DohStringLen */
/* #define StringChar         DohStringChar */
/* #define StringEqual        DohStringEqual */

#define vPrintf            DohvPrintf
#define GetInt             DohGetInt
#define GetDouble          DohGetDouble
#define GetChar            DohGetChar
#define GetVoid            DohGetVoid
#define GetFlagAttr        DohGetFlagAttr
#define GetFlag            DohGetFlag
#define SetInt             DohSetInt
#define SetDouble          DohSetDouble
#define SetChar            DohSetattr
#define SetVoid            DohSetVoid
#define SetFlagAttr        DohSetFlagAttr
#define SetFlag            DohSetFlag
#define UnsetFlag(o,n)     DohSetFlagAttr(o,n,NULL)
#define ClearFlag(o,n)     DohSetFlagAttr(o,n,"")
#define Readline           DohReadline
#define Replace            DohReplace
#define Chop               DohChop
#define Getmeta            DohGetmeta
#define Setmeta            DohSetmeta
#define Delmeta            DohDelmeta
#define NewString          DohNewString
#define NewStringEmpty     DohNewStringEmpty
#define NewStringWithSize  DohNewStringWithSize
#define NewStringf         DohNewStringf
#define NewHash            DohNewHash
#define NewList            DohNewList
#define NewFile            DohNewFile
#define NewFileFromFile    DohNewFileFromFile
#define NewFileFromFd      DohNewFileFromFd
#define FileErrorDisplay   DohFileErrorDisplay
#define NewVoid            DohNewVoid
#define Keys               DohKeys
#define SortedKeys         DohSortedKeys
#define Strcmp             DohStrcmp
#define Strncmp            DohStrncmp
#define Strstr             DohStrstr
#define Strchr             DohStrchr
#define Copyto             DohCopyto
#define CloseAllOpenFiles  DohCloseAllOpenFiles
#define Split              DohSplit
#define SplitLines         DohSplitLines
#define Setmark            DohSetmark
#define Getmark            DohGetmark
#define SetMaxHashExpand   DohSetMaxHashExpand
#define GetMaxHashExpand   DohGetMaxHashExpand
#define None               DohNone
#define Call               DohCall
#define First              DohFirst
#define Next               DohNext
#define Iterator           DohIterator
#define SortList           DohSortList
#define Malloc             DohMalloc
#define Realloc            DohRealloc
#define Calloc             DohCalloc
#define Free               DohFree
#define SetExitHandler     DohSetExitHandler
#define Exit               DohExit
#endif

#ifdef NIL
#undef NIL
#endif

#define NIL  (char *) NULL

/* Defines to allow use of poisoned identifiers.
 *
 * For DOH-internal use only!
 */
#define doh_internal_calloc calloc
#define doh_internal_exit exit
/* doh_internal_free not needed as Free() is a macro defined above. */
#define doh_internal_malloc malloc
#define doh_internal_realloc realloc

#if defined __GNUC__ && defined DOH_POISON
/* Use Malloc(), Realloc(), Calloc(), and Free() instead (which will exit with
 * an error rather than return NULL).
 */