/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 J. Erik Radmall

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <https://www.quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
*/

/*! \file commoditycurve.hpp
    \brief Commodity curve
*/

#ifndef quantlib_commodity_curve_hpp
#define quantlib_commodity_curve_hpp

#include <ql/termstructure.hpp>
#include <ql/experimental/commodities/commoditytype.hpp>
#include <ql/experimental/commodities/unitofmeasure.hpp>
#include <ql/experimental/commodities/exchangecontract.hpp>
#include <ql/currency.hpp>
#include <ql/math/interpolations/forwardflatinterpolation.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>

namespace QuantLib {

    //! Commodity term structure
    class CommodityCurve : public TermStructure {
        friend class CommodityIndex;
      public:
        // constructor
        CommodityCurve(std::string name,
                       CommodityType commodityType,
                       Currency currency,
                       UnitOfMeasure unitOfMeasure,
                       const Calendar& calendar,
                       const std::vector<Date>& dates,
                       std::vector<Real> prices,
                       const DayCounter& dayCounter = Actual365Fixed());

        CommodityCurve(std::string name,
                       CommodityType commodityType,
                       Currency currency,
                       UnitOfMeasure unitOfMeasure,
                       const Calendar& calendar,
                       const DayCounter& dayCounter = Actual365Fixed());

        //! \name Inspectors
        //@{
        const std::string& name() const;
        const CommodityType& commodityType() const;
        const UnitOfMeasure& unitOfMeasure() const;
        const Currency& currency() const;
        Date maxDate() const override;
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& prices() const;
        std::vector<std::pair<Date,Real> > nodes() const;
        bool empty() const;

        void setPrices(std::map<Date, Real>& prices);
        void setBasisOfCurve(
                       const ext::shared_ptr<CommodityCurve>& basisOfCurve);

        Real price(
               const Date& d,
               const ext::shared_ptr<ExchangeContracts>& exchangeContracts,
               Integer nearbyOffset) const;
        Real basisOfPrice(const Date& d) const;
        Date underlyingPriceDate(
                const Date& date,
                const ext::shared_ptr<ExchangeContracts>& exchangeContracts,
                Integer nearbyOffset) const;

        const ext::shared_ptr<CommodityCurve>& basisOfCurve() const;

        friend std::ostream& operator<<(std::ostream& out,
                                        const CommodityCurve& curve);
      protected:
        Real basisOfPriceImpl(Time t) const;

        std::string name_;
        CommodityType commodityType_;
        UnitOfMeasure unitOfMeasure_;
        Currency currency_;
        mutable std::vector<Date> dates_;
        mutable std::vector<Time> times_;
        mutable std::vector<Real> data_;
        mutable Interpolation interpolation_;
        ForwardFlat interpolator_;
        ext::shared_ptr<CommodityCurve> basisOfCurve_;
        Real basisOfCurveUomConversionFactor_;

        Real priceImpl(Time t) cons