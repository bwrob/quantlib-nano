 {
            preAdjustValues();
            postAdjustValues();
        }

        /*! This method returns the times at which the numerical
            method should stop while rolling back the asset. Typical
            examples include payment times, exercise times and such.

            \note The returned values are not guaranteed to be sorted.
        */
        virtual std::vector<Time> mandatoryTimes() const = 0;
        //@}
      protected:
        /*! Indicates if a coupon should be adjusted in preAdjustValues() or postAdjustValues(). */
        enum class CouponAdjustment { pre, post };

        /*! This method checks whether the asset was rolled at the
            given time. */
        bool isOnTime(Time t) const;
        /*! This method performs the actual pre-adjustment */
        virtual void preAdjustValuesImpl() {}
        /*! This method performs the actual post-adjustment */
        virtual void postAdjustValuesImpl() {}

        Time time_;
        Time latestPreAdjustment_, latestPostAdjustment_;
        Array values_;
      private:
        ext::shared_ptr<Lattice> method_;
    };


    //! Useful discretized discount bond asset
    class DiscretizedDiscountBond : public DiscretizedAsset {
      public:
        DiscretizedDiscountBond() = default;
        void reset(Size size) override { values_ = Array(size, 1.0); }
        std::vector<Time> mandatoryTimes() const override { return std::vector<Time>(); }
    };


    //! Discretized option on a given asset
    /*! \warning it is advised that derived classes take care of
                 creating and initializing themselves an instance of
                 the underlying.
    */
    class DiscretizedOption : public DiscretizedAsset {
      public:
        DiscretizedOption(ext::shared_ptr<DiscretizedAsset> underlying,
                          Exercise::Type exerciseType,
                          std::vector<Time> exerciseTimes)
        : underlying_(std::move(underlying)), exerciseType_(exerciseType),
          exerciseTimes_(std::move(exerciseTimes)) {}
        void reset(Size size) override;
        std::vector<Time> mandatoryTimes() const override;

      protected:
        void postAdjustValuesImpl() override;
        void applyExerciseCondition();
        ext::shared_ptr<DiscretizedAsset> underlying_;
        Exercise::Type exerciseType_;
        std::vector<Time> exerciseTimes_;
    };



    // inline definitions

    inline void DiscretizedAsset::initialize(
                             const ext::shared_ptr<Lattice>& method,
                             Time t) {
        method_ = method;
        method_->initialize(*this, t);
    }

    inline void DiscretizedAsset::rollback(Time to) {
        method_->rollback(*this, to);
    }

    inline void DiscretizedAsset::partialRollback(Time to) {
        method_->partialRollback(*this, to);
    }

    inline Real DiscretizedAsset::presentValue() {
        return method_->presentValue(*this);
    }

    inline void DiscretizedAsset::preAdjustValues() {
        if (!close_enough(time(),latestPreAdjustment_)) {
            preAdjustValuesImpl();
            latestPreAdjustment_ = time();
        }
    }

    inline void DiscretizedAsset::postAdjustValues() {
        if (!close_enough(time(),latestPostAdjustment_)) {
            postAdjustValuesImpl();
            latestPostAdjustment_ = time();
        }
    }

    inline bool DiscretizedAsset::isOnTime(Time t) const {
        const TimeGrid& grid = method()->timeGrid();
        return close_enough(grid[grid.index(t)],time());
    }


    inline void DiscretizedOption::reset(Size size) {
        QL_REQUIRE(method() == underlying_->method(),
                   "option and underlying were initialized on "
                   "different methods");
        values_ = Array(size, 0.0);
        adjustValues();
    }

    inline std::vector<Time> DiscretizedOption::mandatoryTimes() const {
        std::vector<Time> times = underlying_->mandatoryTimes();

