al() const { return upperDiagonal_; }
        //@}
        //! \name Modifiers
        //@{
        void setFirstRow(Real, Real);
        void setMidRow(Size, Real, Real, Real);
        void setMidRows(Real, Real, Real);
        void setLastRow(Real, Real);
        void setTime(Time t);
        //@}
        //! \name Utilities
        //@{
        void swap(TridiagonalOperator&) noexcept;
        //@}
        //! encapsulation of time-setting logic
        class TimeSetter {
          public:
            virtual ~TimeSetter() = default;
            virtual void setTime(Time t,
                                 TridiagonalOperator& L) const = 0;
        };
      protected:
        Size n_;
        Array diagonal_, lowerDiagonal_, upperDiagonal_;
        mutable Array temp_;
        ext::shared_ptr<TimeSetter> timeSetter_;
    };

    /* \relates TridiagonalOperator */
    void swap(TridiagonalOperator&, TridiagonalOperator&) noexcept;


    // inline definitions

    inline TridiagonalOperator::TridiagonalOperator(TridiagonalOperator&& from) noexcept : n_(0) {
        swap(from);
    }

    inline TridiagonalOperator& TridiagonalOperator::operator=(
                                const TridiagonalOperator& from) {
        TridiagonalOperator temp(from);
        swap(temp);
        return *this;
    }

    inline TridiagonalOperator&
    TridiagonalOperator::operator=(TridiagonalOperator&& from) noexcept {
        swap(from);
        return *this;
    }

    inline void TridiagonalOperator::setFirstRow(Real valB,
                                                 Real valC) {
        diagonal_[0]      = valB;
        upperDiagonal_[0] = valC;
    }

    inline void TridiagonalOperator::setMidRow(Size i,
                                               Real valA,
                                               Real valB,
                                               Real valC) {
        QL_REQUIRE(i>=1 && i<=n_-2,
                   "out of range in TridiagonalSystem::setMidRow");
        lowerDiagonal_[i-1] = valA;
        diagonal_[i]        = valB;
        upperDiagonal_[i]   = valC;
    }

    inline void TridiagonalOperator::setMidRows(Real valA,
                                                Real valB,
                                                Real valC) {
        for (Size i=1; i<=n_-2; i++) {
            lowerDiagonal_[i-1] = valA;
            diagonal_[i]        = valB;
            upperDiagonal_[i]   = valC;
        }
    }

    inline void TridiagonalOperator::setLastRow(Real valA,
                                                Real valB) {
        lowerDiagonal_[n_-2] = valA;
        diagonal_[n_-1]      = valB;
    }

    inline void TridiagonalOperator::setTime(Time t) {
        if (timeSetter_ != nullptr)
            timeSetter_->setTime(t, *this);
    }

    inline void TridiagonalOperator::swap(TridiagonalOperator& from) noexcept {
        std::swap(n_, from.n_);
        diagonal_.swap(from.diagonal_);
        lowerDiagonal_.swap(from.lowerDiagonal_);
        upperDiagonal_.swap(from.upperDiagonal_);
        temp_.swap(from.temp_);
        timeSetter_.swap(from.timeSetter_);
    }


    // Time constant algebra

    inline TridiagonalOperator operator+(const TridiagonalOperator& D) {
        TridiagonalOperator D1 = D;
        return D1;
    }

    inline TridiagonalOperator operator-(const TridiagonalOperator& D) {
        Array low = -D.lowerDiagonal_,
            mid = -D.diagonal_,
            high = -D.upperDiagonal_;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline TridiagonalOperator operator+(const TridiagonalOperator& D1,
                                         const TridiagonalOperator& D2) {
        Array low = D1.lowerDiagonal_ + D2.lowerDiagonal_,
            mid = D1.diagonal_ + D2.diagonal_,
            high = D1.upperDiagonal_ + D2.upperDiagonal_;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline Tridiagona