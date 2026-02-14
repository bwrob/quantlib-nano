     void applyBeforeSolving(TridiagonalOperator&, Array& rhs) const override;
        void applyAfterSolving(Array&) const override;
        void setTime(Time) override {}

      private:
        Real value_;
        Side side_;
    };

}


#endif