 /*! The ISO three-letter code is XOF; the numeric code is 952.
     It is divided into 100 centime.
     \ingroup currencies
    */
    class XOFCurrency : public Currency {
      public:
        XOFCurrency();
    };

    //! South-African rand
    /*! The ISO three-letter code is ZAR; the numeric code is 710.
        It is divided into 100 cents.

        \ingroup currencies
    */
    class ZARCurrency : public Currency {
      public:
        ZARCurrency();
    };

    //! Zambian kwacha
    /*! The ISO three-letter code is ZMW; the numeric code is 967.
    It is divided into 100 ngwee.
     \ingroup currencies
    */
    class ZMWCurrency : public Currency {
      public:
        ZMWCurrency();
    };

}

#if defined(QL_PATCH_MSVC)
#pragma warning(pop)
#endif

#endif
