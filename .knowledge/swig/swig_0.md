/* ----------------------------------------------------------------------------- 
 * This file is part of SWIG, which is licensed as a whole under version 3 
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * swig.h
 *
 * Header file for the SWIG core.
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_SWIG_H
#define SWIG_SWIG_H

#include "swigconfig.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#ifdef __cplusplus
extern "C" {
#endif

#include "doh.h"

/* Status codes */

#define SWIG_OK         1
#define SWIG_ERROR      0
#define SWIG_NOWRAP     0

/* Global macros */
#define NSPACE_SEPARATOR "." /* Namespace separator for the nspace feature - this should be changed to a target language configurable variable */
#define NSPACE_TODO 0 /* Languages that still need to implement and test the nspace feature use this */

/* Short names for common data types */

  typedef DOH String;
  typedef DOH Hash;
  typedef DOH List;
  typedef DOH String_or_char;
  typedef DOH File;
  typedef DOH Parm;
  typedef DOH ParmList;
  typedef DOH Node;
  typedef DOH Symtab;
  typedef DOH Typetab;
  typedef DOH SwigType;

/* --- Legacy DataType interface.  These type codes are provided solely 
       for backwards compatibility with older modules --- */

/* --- The ordering of type values is used to determine type-promotion 
       in the parser.  Do not change */

/* Numeric types */

#define   T_BOOL       1
#define   T_SCHAR      2
#define   T_UCHAR      3
#define   T_SHORT      4
#define   T_USHORT     5
#define   T_INT        7
#define   T_UINT       8
#define   T_LONG       9
#define   T_ULONG      10
#define   T_LONGLONG   11
#define   T_ULONGLONG  12
#define   T_FLOAT      20
#define   T_DOUBLE     21
#define   T_LONGDOUBLE 22
#define   T_FLTCPLX    23
#define   T_DBLCPLX    24
#define   T_AUTO       26

#define   T_COMPLEX    T_DBLCPLX

/* non-numeric */

#define   T_CHAR       29
#define   T_WCHAR      30
#define   T_USER       31
#define   T_VOID       32
#define   T_STRING     33
#define   T_POINTER    34
#define   T_REFERENCE  35
#define   T_ARRAY      36
#define   T_FUNCTION   37
#define   T_MPOINTER   38
#define   T_VARARGS    39
#define   T_RVALUE_REFERENCE  40
#define   T_WSTRING    41
#define   T_UNKNOWN    42

/* --- File interface --- */

#include "swigfile.h"

/* --- Command line parsing --- */

#include "swigopt.h"

/* --- Scanner Interface --- */

#include "swigscan.h"

/* --- Functions for manipulating the string-based type encoding --- */

  extern SwigType *NewSwigType(int typecode);
  extern SwigType *SwigType_del_element(SwigType *t);
  extern SwigType *SwigType_add_pointer(SwigType *t);
  extern SwigType *SwigType_add_memberpointer(SwigType *t, const_String_or_char_ptr qual);
  extern SwigType *SwigType_del_memberpointer(SwigType *t);
  extern SwigType *SwigType_del_pointer(SwigType *t);
  extern SwigType *SwigType_add_array(SwigType *t, const_String_or_char_ptr size);
  extern SwigType *SwigType_del_array(SwigType *t);
  extern SwigType *SwigType_pop_arrays(SwigType *t);
  extern SwigType *SwigType_add_reference(SwigType *t);
  extern SwigType *SwigType_del_reference(SwigType *t);
  extern SwigType *SwigType_add_rvalue_reference(SwigType *t);
  extern SwigType *SwigType_del_rvalue_reference(SwigType *t);
  extern SwigType *SwigType_add_variadic(SwigType *t);
  extern SwigType *SwigType_del_variadic(SwigType *t);
  extern SwigType *SwigType_add_qualifier(SwigType *t, const_String_or_char_ptr qual);
  extern SwigType *SwigType_del_qualifier(SwigType *t);
  extern SwigType *SwigType_add_function(SwigType *t, ParmList *parms);
  extern SwigType *