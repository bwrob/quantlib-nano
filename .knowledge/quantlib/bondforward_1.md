 considered income.
        */
        Real spotIncome(const Handle<YieldTermStructure>& incomeDiscountCurve) const override;

        //!  NPV of underlying bond
        Real spotValue() const override;

        //@}

      protected:
        ext::shared_ptr<Bond> bond_;
        void performCalculations() const override;
    };

}

#endif
