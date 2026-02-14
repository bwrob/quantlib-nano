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


#ifndef quantlib_kernel_interpolation_hpp
#define quantlib_kernel_interpolation_hpp

#include <ql/math/interpolation.hpp>
#include <ql/math/matrixutilities/qrdecomposition.hpp>
#include <utility>

/*! \file kernelinterpolation.hpp
    \brief Kernel interpolation
*/

namespace QuantLib {

    namespace detail {

        template <class I1, class I2, class Kernel>
        class KernelInterpolationImpl final
            : public Interpolation::templateImpl<I1,I2> {
          public:
            KernelInterpolationImpl(const I1& xBegin,
                                    const I1& xEnd,
                                    const I2& yBegin,
                                    Kernel kernel,
                                    const Real epsilon)
            : Interpolation::templateImpl<I1, I2>(xBegin, xEnd, yBegin),
              xSize_(Size(xEnd - xBegin)), invPrec_(epsilon), M_(xSize_, xSize_), alphaVec_(xSize_),
              yVec_(xSize_), kernel_(std::move(kernel)) {}

            void update() override { updateAlphaVec(); }

            Real value(Real x) const override {

                Real res=0.0;

                for( Size i=0; i< xSize_;++i){
                    res+=alphaVec_[i]*kernelAbs(x,this->xBegin_[i]);
                }

                return res/gammaFunc(x);
            }

            Real primitive(Real) const override {
                QL_FAIL("Primitive calculation not implemented "
                        "for kernel interpolation");
            }

            Real derivative(Real) const override {
                QL_FAIL("First derivative calculation not implemented "
                        "for kernel interpolation");
            }

            Real secondDerivative(Real) const override {
                QL_FAIL("Second derivative calculation not implemented "
                        "for kernel interpolation");
            }

        private:

            Real kernelAbs(Real x1, Real x2)const{
                return kernel_(std::fabs(x1-x2));
            }

            Real gammaFunc(Real x)const{

                Real res=0.0;

                for(Size i=0; i< xSize_;++i){
                    res+=kernelAbs(x,this->xBegin_[i]);
                }
                return res;
            }

            void updateAlphaVec(){
                // Function calculates the alpha vector with given
                // fixed pillars+values

                // Write Matrix M
                Real tmp=0.0;

                for(Size rowIt=0; rowIt<xSize_;++rowIt){

                    yVec_[rowIt]=this->yBegin_[rowIt];
                    tmp=1.0/gammaFunc(this->xBegin_[rowIt]);

                    for(Size colIt=0; colIt<xSize_;++colIt){
                        M_[rowIt][colIt]=kernelAbs(this->xBegin_[rowIt],
                                                   this->xBegin_[colIt])*tmp;
                    }
                }

                // Solve y=M*\alpha for \alpha
                alphaVec_ = qrSolve(M_, yVec_);

                // check if inversion worked up to a reasonable precision.
                // I've chosen not to check determinant(M_)!=0 before solving

                Array diffVec=Abs(M_*alphaVec_ -