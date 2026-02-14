/* -----------------------------------------------------------------------------
 * This file is part of SWIG, which is licensed as a whole under version 3
 * (or any later version) of the GNU General Public License. Some additional
 * terms also apply to certain portions of SWIG. The full details of the SWIG
 * license and copyrights can be found in the LICENSE and COPYRIGHT files
 * included with the SWIG source code as distributed by the SWIG developers
 * and at https://www.swig.org/legal.html.
 *
 * swigwarn.h
 *
 * SWIG warning message numbers
 * This file serves as the main registry of warning message numbers.  Some of these
 * numbers are used internally in the C/C++ source code of SWIG.   However, some
 * of the numbers are used in SWIG configuration files (swig.swg and others).
 *
 * The numbers are roughly organized into a few different classes by functionality.
 *
 * Even though symbolic constants are used in the SWIG source, this is
 * not always the case in SWIG interface files.  Do not change the
 * numbers in this file.
 *
 * This file is used as the input for generating Lib/swigwarn.swg.
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_SWIGWARN_H
#define SWIG_SWIGWARN_H

#define WARN_NONE                     0

/* -- Deprecated features -- */

/* Unused since 4.2.0: #define WARN_DEPRECATED_EXTERN        101 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_VAL           102 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_OUT           103 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_DISABLEDOC    104 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_ENABLEDOC     105 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_DOCONLY       106 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_STYLE         107 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_LOCALSTYLE    108 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_TITLE         109 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_SECTION       110 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_SUBSECTION    111 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_SUBSUBSECTION 112 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_ADDMETHODS    113 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_READONLY      114 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_READWRITE     115 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_EXCEPT        116 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_NEW           117 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_EXCEPT_TM     118 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_IGNORE_TM     119 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_OPTC          120 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_NAME          121 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_NOEXTERN      122 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_NODEFAULT     123 */
/* Unused since 4.1.0: #define WARN_DEPRECATED_TYPEMAP_LANG  124 */
/* Unused since 4.2.0: #define WARN_DEPRECATED_INPUT_FILE    125 */
/* Unused since 4.3.0: #define WARN_DEPRECATED_NESTED_WORKAROUND 126 */
#define WARN_DEPRECATED_TYPEDEF 127

/* -- Preprocessor -- */

#define WARN_PP_MISSING_FILE          201
#define WARN_PP_EVALUATION            202
#define WARN_PP_INCLUDEALL_IMPORTALL  203
#define WARN_PP_CPP_WARNING           204
#define WARN_PP_CPP_ERROR             205
#define WARN_PP_UNEXPECTED_TOKENS     206

/* -- C/C++ Parser -- */

#define WARN_PARSE_CLASS_KEYWORD      301
#define WARN_PARSE_REDEFINED          302
#define WARN_PARSE_EXTEND_UNDEF       303
#define WARN_PARSE_UNSUPPORTED_VALUE  304
#define WARN_PARSE_BAD_VALUE          305
/* Unused since 1.3.32: #define WARN_PARSE_PRIVATE            306 */
/* Unused since 4.2.0: #define WARN_PARSE_BAD_DEFAULT        307 */
#define WARN_PARSE_NAMESPACE_ALIAS    308
#define WARN_PARSE_PRIVATE_INHERIT    309
/* Unused since 1.3.18: #define WARN_PARSE_TEMPLATE_REPEAT    310 */
/* Unused since 1.3.18: #define WARN_PARSE_TEMPLATE_PART