/* -*- mode: c; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/* this file is a slightly edited version of
 * PrimitivePolynomialsModuloTwoUpToDegree27.h
 * © 2002 "Monte Carlo Methods in Finance"
 * as provided ready for compilation in the directory
 * "PrimitivePolynomialsModuloTwo" on the CD accompanying the book
 * "Monte Carlo Methods in Finance" by Peter Jäckel.
 *
 * ===========================================================================
 * NOTE: The following copyright notice applies to the original code,
 *
 * Copyright (C) 2002 Peter Jäckel "Monte Carlo Methods in Finance".
 * All rights reserved.
 *
 * Permission to use, copy, modify, and distribute this software is freely
 * granted, provided that this notice is preserved.
 * ===========================================================================
 */
#ifndef primitivepolynomials_hpp
#define primitivepolynomials_hpp

/* This file is provided for the use with Sobol' sequences of higher
 * dimensions. The dimensionality of the Sobol' sequence can be extended to
 * virtually any size you ever might need by the aid of the table of
 * primitive polynomials modulo two.
 * It is up to you to define a macro PPMT_MAX_DIM to a positive integer
 * less than or equal to 8129334. If you don't define it, it will be set
 * below to N_PRIMITIVES_UP_TO_DEGREE_18 which is 21200. That's how many
 * primitive polynomials are provided by the standard primitivepolynomial.c
 * distributed with QuantLib and that will be compiled into a static array.
 * Should you need more, get the original version of primitivepolynomial.c
 * as provided ready for compilation in the directory
 * "PrimitivePolynomialsModuloTwo" on the CD accompanying the book
 * "Monte Carlo Methods in Finance" by Peter Jäckel.
 * The file provides polynomials up to degree 27
 * for a grand total of 8129334 dimensions.
 * Since 8129334 longs compile into an object file of at least 32517336 byte
 * size (in fact, gcc -c -O0 PrimitivePolynomialsModuloTwoUpToDegree27.c
 * produced a file PrimitivePolynomialsModuloTwoUpToDegree27.o with 32519920
 * bytes), it is recommended to only compile as many as you may ever need.
 * Worse even than the output file size is the virtual memory requirement
 * for the compilation. For Visual C++ 6 you will need to use the /Zm compiler
 * option to set the compiler's memory allocation limit (/Zm1500 should work)
 * So really only take the maximum of what you think you might ever need.
 * After all, you can always recompile with more, should you need it.
 */

/*  PPMT : Primitive Polynomials Modulo Two
 *
 *
 * The encoding is as follows:
 *
 * The coefficients of each primitive polynomial are the bits of the given
 * integer. The leading and trailing coefficients, which are 1 for all of the
 * polynomials, have been omitted.
 *
 * Example: The polynomial
 *
 *      4    2
 *     x  + x  + 1
 *
 * is encoded as  2  in the array of polynomials of degree 4 because the
 * binary sequence of coefficients
 *
 *   10101
 *
 * becomes
 *
 *    0101
 *
 * after stripping off the top bit, and this is converted to
 *
 *     010
 *
 * by right-shifting and losing the rightmost bit. Similarly, we have
 *
 *   5    4    2
 *  x  + x  + x  + x + 1
 *
 * encoded as  13  [ (1)1101(1) ]  in the array for degree 5.
 */

/* Example: replace primitivepolynomials.cpp provided by QuantLib standard
 * distribution with the 8129334 polinomials version and
 * comment out the line below if you want absolutely all of the
 * provided primitive polynomials modulo two.
 *
 * #define PPMT_MAX_DIM 8129334
 *
 * Note that PPMT_MAX_DIM will be redefined to be the nearest equal or larger
 * number of polynomials up to one of the predefined macros
 * N_PRIMITIVES_UP_TO_DEGREE_XX
 * below.
 */


#define N_PRIMITIVES_UP_TO_DEGREE_01         1
#define N_PRIMITIVES_UP_TO_DEGREE_02         2
#define N_PRIMITIVES_UP_TO_DEGREE_03         4
#define N_PRIMITIVES_UP_TO_DEGREE_04         6
#define N_PRIMITIVES_UP_TO_