ecision,
                            Integer digit = 5)
        : Rounding(precision,Up,digit) {}
    };

    //! Down-rounding.
    class DownRounding : public Rounding {
      public:
        explicit DownRounding(Integer precision,
                              Integer digit = 5)
        : Rounding(precision,Down,digit) {}
    };

    //! Closest rounding.
    class ClosestRounding : public Rounding {
      public:
        explicit ClosestRounding(Integer precision,
                                 Integer digit = 5)
        : Rounding(precision,Closest,digit) {}
    };

    //! Ceiling truncation.
    class CeilingTruncation : public Rounding {
      public:
        explicit CeilingTruncation(Integer precision,
                                   Integer digit = 5)
        : Rounding(precision,Ceiling,digit) {}
    };

    //! %Floor truncation.
    class FloorTruncation : public Rounding {
      public:
        explicit FloorTruncation(Integer precision,
                                 Integer digit = 5)
        : Rounding(precision,Floor,digit) {}
    };

}


#endif
