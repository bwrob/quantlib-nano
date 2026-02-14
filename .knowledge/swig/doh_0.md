/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3 
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * doh.h
 *
 *     This file describes of the externally visible functions in DOH.
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_DOH_H
#define SWIG_DOH_H

#include "swigconfig.h"

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

/* Set the namespace prefix for DOH API functions. This can be used to control
   visibility of the functions in libraries */

/* Set this macro if you want to change DOH linkage. You would do this if you
   wanted to hide DOH in a library using a different set of names.  Note: simply
   change "Doh" to a new name. */

/*
#define DOH_NAMESPACE(x) Doh ## x
*/

#ifdef DOH_NAMESPACE

/* Namespace control.  These macros define all of the public API names in DOH */

#define DohCheck           DOH_NAMESPACE(Check)
#define DohIntern          DOH_NAMESPACE(Intern)
#define DohDelete          DOH_NAMESPACE(Delete)
#define DohCopy            DOH_NAMESPACE(Copy)
#define DohClear           DOH_NAMESPACE(Clear)
#define DohStr             DOH_NAMESPACE(Str)
#define DohData            DOH_NAMESPACE(Data)
#define DohDump            DOH_NAMESPACE(Dump)
#define DohLen             DOH_NAMESPACE(Len)
#define DohHashval         DOH_NAMESPACE(Hashval)
#define DohCmp             DOH_NAMESPACE(Cmp)
#define DohEqual           DOH_NAMESPACE(Equal)
#define DohIncref          DOH_NAMESPACE(Incref)
#define DohCheckattr       DOH_NAMESPACE(Checkattr)
#define DohSetattr         DOH_NAMESPACE(Setattr)
#define DohDelattr         DOH_NAMESPACE(Delattr)
#define DohKeys            DOH_NAMESPACE(Keys)
#define DohSortedKeys      DOH_NAMESPACE(SortedKeys)
#define DohGetInt          DOH_NAMESPACE(GetInt)
#define DohGetDouble       DOH_NAMESPACE(GetDouble)
#define DohGetChar         DOH_NAMESPACE(GetChar)
#define DohSetChar         DOH_NAMESPACE(SetChar)
#define DohSetInt          DOH_NAMESPACE(SetInt)
#define DohSetDouble       DOH_NAMESPACE(SetDouble)
#define DohSetVoid         DOH_NAMESPACE(SetVoid)
#define DohGetVoid         DOH_NAMESPACE(GetVoid)
#define DohGetitem         DOH_NAMESPACE(Getitem)
#define DohSetitem         DOH_NAMESPACE(Setitem)
#define DohDelitem         DOH_NAMESPACE(Delitem)
#define DohInsertitem      DOH_NAMESPACE(Insertitem)
#define DohDelslice        DOH_NAMESPACE(Delslice)
#define DohWrite           DOH_NAMESPACE(Write)
#define DohRead            DOH_NAMESPACE(Read)
#define DohSeek            DOH_NAMESPACE(Seek)
#define DohTell            DOH_NAMESPACE(Tell)
#define DohGetc            DOH_NAMESPACE(Getc)
#define DohPutc            DOH_NAMESPACE(Putc)
#define DohUngetc          DOH_NAMESPACE(Ungetc)
#define DohGetline         DOH_NAMESPACE(Getline)
#define DohSetline         DOH_NAMESPACE(Setline)
#define DohGetfile         DOH_NAMESPACE(Getfile)
#define DohSetfile         DOH_NAMESPACE(Setfile)
#define DohReplace         DOH_NAMESPACE(Replace)
#define DohChop            DOH_NAMESPACE(Chop)
#define DohGetmeta         DOH_NAMESPACE(Getmeta)
#define DohSetmeta         DOH_NAMESPACE(Setmeta)
#define DohDelmeta         DOH_NAMESPACE(Delmeta)
#define DohEncoding        DOH_NAMESPACE(Encoding)
#define DohPrintf          DOH_NAMESPACE(Printf)
#define DohvPrintf         DOH_NAMESPACE(vPrintf)
#define DohPrintv          DOH_NAMESPACE(Printv)
#define DohReadline        DOH_NAMESPACE(Readline)
#define DohIsMapping       DOH_NAMESPACE(IsMapping)
#define DohIsSequence      DOH_NAMESPACE(IsSequence)
#define DohIsString        DOH_NAMESPACE(IsString)
#define DohIsFile    