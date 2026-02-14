/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#ifndef quantlib_spread_discount_curve_hpp
#define quantlib_spread_discount_curve_hpp

#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/math/interpolations/loginterpolation.hpp>
#include <utility>

namespace QuantLib {

    //! Yield curve based on interpolation of discount factors applied as
    //! a multiplicative spread to the base YieldTermStructure
    /*! The discount factors spread at any given date is interpolated
        between the input data.

        \note This term structure will remain linked to the original
              structure, i.e., any changes in the latter will be
              reflected in this structure as well.

        \ingroup yieldtermstructures
    */

    template <class Interpolator>
    class InterpolatedSpreadDiscountCurve
        : public YieldTermStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedSpreadDiscountCurve(
            Handle<YieldTermStructure> baseCurve,
            std::vector<Date> dates,
            std::vector<DiscountFactor> dfs,
            const Interpolator& interpolator = {});
        //! \name YieldTermStructure interface
        //@{
        DayCounter dayCounter() const override;
        Natural settlementDays() const override;
        Calendar calendar() const override;
        const Date& referenceDate() const override;
        Date maxDate() const override;
        //@}
        //@}
        //! \name other inspectors
        //@{
        const Handle<YieldTermStructure>& baseCurve() const;
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        std::vector<std::pair<Date, Real>> nodes() const;
        //@}
      protected:
        InterpolatedSpreadDiscountCurve(
            Handle<YieldTermStructure> baseCurve,
            const Interpolator& interpolator);
        //! \name YieldTermStructure implementation
        //@{
        DiscountFactor discountImpl(Time) const override;
        //@}
        void update() override;

        mutable std::vector<Date> dates_;
      private:
        void updateInterpolation();
        DiscountFactor calcSpread(Time t) const;

        Handle<YieldTermStructure> baseCurve_;
        DayCounter prevDayCount_;
    };

    //! Spread yield curve based on log-linear interpolation of discount factors
    /*! Log-linear interpolation guarantees piecewise-constant spreads.

        \ingroup yieldtermstructures
    */
    typedef InterpolatedSpreadDiscountCurve<LogLinear> SpreadDiscountCurve;


    // inline definitions

    #ifndef __DOXYGEN__

    template <class T>
    inline InterpolatedSpreadDiscountCurve<T>::InterpolatedSpreadDiscountCurve(
        Handle<YieldTermStructure> baseCurve,
        std::vector<Date> dates,
        std::vector<DiscountFactor> dfs,
        const T& interpolator)
    : InterpolatedCurve<T>({}, std::move(dfs), interpolator),
      dates_(std::move(dates)), baseCurve_(std::move(baseCurve)) {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");
        QL_REQUIRE(this->data_[0] == 1.0,
                   "the first discount must be == 1.0 "
                   "to flag the corresponding date as reference date");
        for (Size i = 1; i < dates_.size(); ++i) {
            QL_REQUIRE(this->data_[i] > 0.0, "negative discount");
        }

        registerWith(baseCurve_);
        if (!baseCurve_.empty())
            updateInterpolation();
    }

    template <class T>
    inline InterpolatedSpreadDiscountCurve<T>::InterpolatedSpreadDiscountCurve(
        Handle<YieldTermStructure> baseCurve,
        const T& interpolator)
    : InterpolatedCurve<T>(interpolator), baseC
