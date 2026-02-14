r:1;	/* User flag */
  unsigned int flag_usermark:1;	/* User marked */
  unsigned int refcount:28;	/* Reference count (max 256 million) */
} DohBase;

/* Macros for decrefing and increfing (safe for null objects). */

#define Decref(a)         if (a) ((DohBase *) a)->refcount--
#define Incref(a)         if (a) ((DohBase *) a)->refcount++
#define Refcount(a)       ((DohBase *) a)->refcount

/* Macros for manipulating objects in a safe manner */
#define ObjData(a)        ((DohBase *)a)->data
#define ObjSetMark(a,x)   ((DohBase *)a)->flag_marked = x
#define ObjGetMark(a)     ((DohBase *)a)->flag_marked
#define ObjType(a)        ((DohBase *)a)->type

extern DOH *DohObjMalloc(DohObjInfo *type, void *data);	/* Allocate a DOH object */
extern void DohObjFree(DOH *ptr);	/* Free a DOH object     */

#endif				/* SWIG_DOHINT_H */