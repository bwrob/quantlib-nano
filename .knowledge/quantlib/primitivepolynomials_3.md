# define PPMT_MAX_DIM N_PRIMITIVES_UP_TO_DEGREE_25

# define N_MAX_DEGREE 25
#elif    PPMT_MAX_DIM <= N_PRIMITIVES_UP_TO_DEGREE_26

# undef  PPMT_MAX_DIM

# define PPMT_MAX_DIM N_PRIMITIVES_UP_TO_DEGREE_26

# define N_MAX_DEGREE 26
#else

# undef  PPMT_MAX_DIM

# define PPMT_MAX_DIM N_PRIMITIVES_UP_TO_DEGREE_27

# define N_MAX_DEGREE 27
#endif

/* Microsoft Visual C++ 6.0 */
#if defined(_MSC_VER)
    /* disable useless warning C4049
       compiler limit : terminating line number emission
       No line number support is available for file with more
       than 64K source lines. */
    #pragma warning(disable: 4049)
#endif

extern

#ifdef __cplusplus

"C"

#endif

/*! You can access the following array as in PrimitivePolynomials[i][j]
    with i and j counting from 0 in C convention. PrimitivePolynomials[i][j]
    will get you the j-th (counting from zero) primitive polynomial of degree
    i+1. Each one-dimensional array of primitive polynomials of a given
    degree is terminated with an entry of -1. Accessing beyond this entry
    will result in a memory violation and must be avoided.  */
const long *const PrimitivePolynomials[N_MAX_DEGREE];

#endif