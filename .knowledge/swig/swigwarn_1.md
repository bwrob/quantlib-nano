IAL   311 */
#define WARN_PARSE_UNNAMED_NESTED_CLASS 312
#define WARN_PARSE_UNDEFINED_EXTERN   313
#define WARN_PARSE_KEYWORD            314
#define WARN_PARSE_USING_UNDEF        315
/* Unused since 1.3.18: #define WARN_PARSE_MODULE_REPEAT      316 */
#define WARN_PARSE_TEMPLATE_SP_UNDEF  317
#define WARN_PARSE_TEMPLATE_AMBIG     318
#define WARN_PARSE_NO_ACCESS          319
#define WARN_PARSE_EXPLICIT_TEMPLATE  320
#define WARN_PARSE_BUILTIN_NAME       321
#define WARN_PARSE_REDUNDANT          322
#define WARN_PARSE_REC_INHERITANCE    323
#define WARN_PARSE_NESTED_TEMPLATE    324
#define WARN_PARSE_NAMED_NESTED_CLASS 325
#define WARN_PARSE_EXTEND_NAME        326
#define WARN_PARSE_EXTERN_TEMPLATE    327
#define WARN_PARSE_ASSIGNED_VALUE     328
#define WARN_PARSE_USING_CONSTRUCTOR  329
#define WARN_PARSE_TEMPLATE_FORWARD   330
#define WARN_PARSE_TEMPLATE_NESTED    331

#define WARN_CPP11_LAMBDA             340
/* Unused since 3.0.11: #define WARN_CPP11_ALIAS_DECLARATION  341 */
/* Unused since 3.0.11: #define WARN_CPP11_ALIAS_TEMPLATE     342 */
/* Unused since 4.2.0: #define WARN_CPP11_VARIADIC_TEMPLATE  343 */
#define WARN_CPP11_DECLTYPE           344
#define WARN_CPP14_AUTO               345
#define WARN_CPP11_AUTO               346

#define WARN_IGNORE_OPERATOR_NEW        350	/* new */
#define WARN_IGNORE_OPERATOR_DELETE     351	/* delete */
#define WARN_IGNORE_OPERATOR_PLUS       352	/* + */
#define WARN_IGNORE_OPERATOR_MINUS      353	/* - */
#define WARN_IGNORE_OPERATOR_MUL        354	/* * */
#define WARN_IGNORE_OPERATOR_DIV        355	/* / */
#define WARN_IGNORE_OPERATOR_MOD        356	/* % */
#define WARN_IGNORE_OPERATOR_XOR        357	/* ^ */
#define WARN_IGNORE_OPERATOR_AND        358	/* & */
#define WARN_IGNORE_OPERATOR_OR         359	/* | */
#define WARN_IGNORE_OPERATOR_NOT        360	/* ~ */
#define WARN_IGNORE_OPERATOR_LNOT       361	/* ! */
#define WARN_IGNORE_OPERATOR_EQ         362	/* = */
#define WARN_IGNORE_OPERATOR_LT         363	/* < */
#define WARN_IGNORE_OPERATOR_GT         364	/* > */
#define WARN_IGNORE_OPERATOR_PLUSEQ     365	/* += */
#define WARN_IGNORE_OPERATOR_MINUSEQ    366	/* -= */
#define WARN_IGNORE_OPERATOR_MULEQ      367	/* *= */
#define WARN_IGNORE_OPERATOR_DIVEQ      368	/* /= */
#define WARN_IGNORE_OPERATOR_MODEQ      369	/* %= */
#define WARN_IGNORE_OPERATOR_XOREQ      370	/* ^= */
#define WARN_IGNORE_OPERATOR_ANDEQ      371	/* &= */
#define WARN_IGNORE_OPERATOR_OREQ       372	/* |= */
#define WARN_IGNORE_OPERATOR_LSHIFT     373	/* << */
#define WARN_IGNORE_OPERATOR_RSHIFT     374	/* >> */
#define WARN_IGNORE_OPERATOR_LSHIFTEQ   375	/* <<= */
#define WARN_IGNORE_OPERATOR_RSHIFTEQ   376	/* >>= */
#define WARN_IGNORE_OPERATOR_EQUALTO    377	/* == */
#define WARN_IGNORE_OPERATOR_NOTEQUAL   378	/* != */
#define WARN_IGNORE_OPERATOR_LTEQUAL    379	/* <= */
#define WARN_IGNORE_OPERATOR_GTEQUAL    380	/* >= */
#define WARN_IGNORE_OPERATOR_LAND       381	/* && */
#define WARN_IGNORE_OPERATOR_LOR        382	/* || */
#define WARN_IGNORE_OPERATOR_PLUSPLUS   383	/* ++ */
#define WARN_IGNORE_OPERATOR_MINUSMINUS 384	/* -- */
#define WARN_IGNORE_OPERATOR_COMMA      385	/* , */
#define WARN_IGNORE_OPERATOR_ARROWSTAR  386	/* ->* */
#define WARN_IGNORE_OPERATOR_ARROW      387	/* -> */
#define WARN_IGNORE_OPERATOR_CALL       388	/* () */
#define WARN_IGNORE_OPERATOR_INDEX      389	/* [] */
#define WARN_IGNORE_OPERATOR_UPLUS      390	/* + */
#define WARN_IGNORE_OPERATOR_UMINUS     391	/* - */
#define WARN_IGNORE_OPERATOR_UMUL       392	/* * */
#define WARN_IGNORE_OPERATOR_UAND       393	/* & */
#define WARN_IGNORE_OPERATOR_NEWARR     394	/* new [] */
#define WARN_IGNORE_OPERATOR_DELARR     395	/* delete [] */
#define WARN_IGNORE_OPERATOR_REF        396	/* operator *() */
#define WARN_IGNORE_OPERATOR_LTEQUALGT  397	/* <=> */

/* please leave 350-399 free for WARN_IGNORE_OPERATOR_* */

/* -- Type system and typemaps -- */

#define WARN_TYPE_UNDEFINED_CLASS     401
#define WARN_TYPE_INCOMPLETE          402
#de