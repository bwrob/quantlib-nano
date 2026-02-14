*/
    class PTECurrency : public Currency {
      public:
        PTECurrency();
    };

    //! Slovak koruna
    /*! The ISO three-letter code is SKK; the numeric code is 703.
        It was divided in 100 halierov.

        Obsoleted by the Euro since 2009.

        \ingroup currencies
    */
    class SKKCurrency : public Currency {
      public:
        SKKCurrency();
    };

}

#if defined(QL_PATCH_MSVC)
#pragma warning(pop)
#endif

#endif
