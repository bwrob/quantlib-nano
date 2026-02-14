rrency {
      public:
        TTDCurrency();
    };

    //! U.S. dollar
    /*! The ISO three-letter code is USD; the numeric code is 840.
        It is divided in 100 cents.

        \ingroup currencies
    */
    class USDCurrency : public Currency {
      public:
        USDCurrency();
    };

    //! Venezuelan bolivar
    /*! The ISO three-letter code is VEB; the numeric code is 862.
        It is divided in 100 centimos.

        \ingroup currencies
    */
    class VEBCurrency : public Currency {
      public:
        VEBCurrency();
    };
    //! Mexican Unidad de Inversion
    /*! The ISO three-letter code is MXV; the numeric code is 979.
     A unit of account used in Mexico.
     \ingroup currencies
    */
    class MXVCurrency : public Currency {
      public:
        MXVCurrency();
    };

    //! Unidad de Valor Real
    /*! The ISO three-letter code is COU; the numeric code is 970.
     A unit of account used in Colombia.
     \ingroup currencies
    */
    class COUCurrency : public Currency {
      public:
        COUCurrency();
    };

    //! Unidad de Fomento (funds code)
    /*! The ISO three-letter code is CLF; the numeric code is 990.
     A unit of account used in Chile.
     \ingroup currencies
     */
    class CLFCurrency : public Currency {
      public:
        CLFCurrency();
    };

    //! Uruguayan peso
    /*! The ISO three-letter code is UYU; the numeric code is 858.
     A unit of account used in Uruguay.
     \ingroup currencies
     */
    class UYUCurrency : public Currency {
      public:
        UYUCurrency();
    };

}

#if defined(QL_PATCH_MSVC)
#pragma warning(pop)
#endif

#endif
