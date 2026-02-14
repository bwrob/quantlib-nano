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

/*! \file quantity.hpp
    \brief Amount of a commodity
*/

#ifndef quantlib_quantity_hpp
#define quantlib_quantity_hpp

#include <ql/experimental/commodities/commoditytype.hpp>
#include <ql/experimental/commodities/unitofmeasure.hpp>
#include <utility>

namespace QuantLib {

    //! Amount of a commodity
    class Quantity {
      public:
        //! \name Constructors
        //@{
        Quantity() = default;
        Quantity(CommodityType commodityType, UnitOfMeasure unitOfMeasure, Real amount);
        //@}
        //! \name Inspectors
        //@{
        const CommodityType& commodityType() const;
        const UnitOfMeasure& unitOfMeasure() const;
        Real amount() const;
        Quantity rounded() const;
        //@}
        /*! \name Quantity arithmetics

            See below for non-member functions and for settings which
            determine the behavior of the operators.
        */
        //@{
        Quantity operator+() const;
        Quantity operator-() const;
        Quantity& operator+=(const Quantity&);
        Quantity& operator-=(const Quantity&);
        Quantity& operator*=(Real);
        Quantity& operator/=(Real);
        //@}
        /*! \name Conversion settings

            These parameters are used for combining quantity amounts
            in different currencies
        */
        //@{
        enum ConversionType {
            NoConversion,                /*!< do not perform conversions */
            BaseUnitOfMeasureConversion, /*!< convert both operands to
                                              the base unitOfMeasure before
                                              converting */
            AutomatedConversion          /*!< return the result in the
                                              unitOfMeasure of the first
                                              operand */
        };
        static ConversionType conversionType;
        static UnitOfMeasure baseUnitOfMeasure;
        //@}

        friend std::ostream& operator<<(std::ostream&, const Quantity&);
      private:
        CommodityType commodityType_;
        UnitOfMeasure unitOfMeasure_;
        Real amount_ = 0.0;
    };


    // More arithmetics and comparisons

    /*! \relates Quantity */
    Quantity operator+(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    Quantity operator-(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    Quantity operator*(const Quantity&, Real);
    /*! \relates Quantity */
    Quantity operator*(Real, const Quantity&);
    /*! \relates Quantity */
    Quantity operator/(const Quantity&, Real);
    /*! \relates Quantity */
    Real operator/(const Quantity&, const Quantity&);

    /*! \relates Quantity */
    bool operator==(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    bool operator!=(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    bool operator<(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    bool operator<=(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    bool operator>(const Quantity&, const Quantity&);
    /*! \relates Quantity */
    bool operator>=(const Quantity&, co
