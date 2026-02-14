/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Dimitri Reiswich

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

/*! \file kernelinterpolation2d.hpp
    \brief 2D Kernel interpolation
*/

#ifndef quantlib_kernel_interpolation2D_hpp
#define quantlib_kernel_interpolation2D_hpp

#include <ql/math/interpolations/interpolation2d.hpp>
#include <ql/math/matrixutilities/qrdecomposition.hpp>
#include <utility>

/*
  Grid Explanation:

  Grid=[  (x1,y1) (x1,y2) (x1,y3)... (x1,yM);
          (x2,y1) (x2,y2) (x2,y3)... (x2,yM);
          .
          .
          .
          (xN,y1) (xN,y2) (xN,y3)... (xN,yM);
       ]

  The Passed variables are:
  - x which is N dimensional
  - y which is M dimensional
  - zData which is NxM dimensional and has the z values
    corresponding to the grid above.
  - kernel is a template which needs a Real operator()(Real x) implementation
*/


namespace QuantLib {

    namespace detail {

        template <class I1, class I2, class M, class Kernel>
        class KernelInterpolation2DImpl
            : public Interpolation2D::templateImpl<I1,I2,M> {

          public:
            KernelInterpolation2DImpl(const I1& xBegin,
                                      const I1& xEnd,
                                      const I2& yBegin,
                                      const I2& yEnd,
                                      const M& zData,
                                      Kernel kernel)
            : Interpolation2D::templateImpl<I1, I2, M>(xBegin, xEnd, yBegin, yEnd, zData),
              xSize_(Size(xEnd - xBegin)), ySize_(Size(yEnd - yBegin)), xySize_(xSize_ * ySize_),
              alphaVec_(xySize_), yVec_(xySize_), M_(xySize_, xySize_), kernel_(std::move(kernel)) {

                QL_REQUIRE(zData.rows()==xSize_,
                           "Z value matrix has wrong number of rows");
                QL_REQUIRE(zData.columns()==ySize_,
                           "Z value matrix has wrong number of columns");
            }

            void calculate() override { updateAlphaVec(); }

            Real value(Real x1, Real x2) const override {

                Real res=0.0;

                Array X(2),Xn(2);
                X[0]=x1;X[1]=x2;

                Size cnt=0; // counter

                for( Size j=0; j< ySize_;++j){
                    for( Size i=0; i< xSize_;++i){
                        Xn[0]=this->xBegin_[i];
                        Xn[1]=this->yBegin_[j];
                        res+=alphaVec_[cnt]*kernelAbs(X,Xn);
                        cnt++;
                    }
                }
                return res/gammaFunc(X);
            }

            // the calculation will solve y=M*a for a.  Due to
            // singularity or rounding errors the recalculation
            // M*a may not give y. Here, a failure will be thrown if
            // |M*a-y|>=invPrec_
            void setInverseResultPrecision(Real invPrec){
                invPrec_=invPrec;
            }

        private:

            // returns K(||X-Y||) where X,Y are vectors
            Real kernelAbs(const Array& X, const Array& Y)const{
                return kernel_(Norm2(X-Y));
            }

            Real gammaFunc(const Array& X)const{

                Real res=0.0;
                Array Xn(X.size());

                for(Size j=0;
