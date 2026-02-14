   }

    inline bool operator!=(const UnitOfMeasure& c1, const UnitOfMeasure& c2) {
        return !(c1 == c2);
    }

    class LotUnitOfMeasure : public UnitOfMeasure {
      public:
        LotUnitOfMeasure() {
            static ext::shared_ptr<Data> data(
                new Data("Lot", "Lot", UnitOfMeasure::Quantity));
            data_ = data;
        }
    };

}


#endif