j< ySize_;++j){
                    for(Size i=0; i< xSize_;++i){
                        Xn[0]=this->xBegin_[i];
                        Xn[1]=this->yBegin_[j];
                        res+=kernelAbs(X,Xn);
                    }
                }

                return res;
            }

            void updateAlphaVec(){
                // Function calculates the alpha vector with given
                // fixed pillars+values

                Array Xk(2),Xn(2);

                Size rowCnt=0,colCnt=0;
                Real tmpVar=0.0;

                // write y-vector and M-Matrix
                for(Size j=0; j< ySize_;++j){
                    for(Size i=0; i< xSize_;++i){

                        yVec_[rowCnt]=this->zData_[i][j];
                        // calculate X_k
                        Xk[0]=this->xBegin_[i];
                        Xk[1]=this->yBegin_[j];

                        tmpVar=1/gammaFunc(Xk);
                        colCnt=0;

                        for(Size jM=0; jM< ySize_;++jM){
                            for(Size iM=0; iM< xSize_;++iM){
                                Xn[0]=this->xBegin_[iM];
                                Xn[1]=this->yBegin_[jM];
                                M_[rowCnt][colCnt]=kernelAbs(Xk,Xn)*tmpVar;
                                colCnt++; // increase column counter
                            }// end iM
                        }// end jM
                        rowCnt++; // increase row counter
                    } // end i
                }// end j

                alphaVec_=qrSolve(M_, yVec_);

                // check if inversion worked up to a reasonable precision.
                // I've chosen not to check determinant(M_)!=0 before solving

                Array diffVec=Abs(M_*alphaVec_ - yVec_);
                for (Real i : diffVec) {
                    QL_REQUIRE(i < invPrec_, "inversion failed in 2d kernel interpolation");
                }
            }


            Size xSize_,ySize_,xySize_;
            Real invPrec_ = 1.0e-10;
            Array alphaVec_, yVec_;
            Matrix M_;
            Kernel kernel_;
        };

    } // end namespace detail


    /*! Implementation of the 2D kernel interpolation approach, which
        can be found in "Foreign Exchange Risk" by Hakala, Wystup page
        256.

        The kernel in the implementation is kept general, although a
        Gaussian is considered in the cited text.

        \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class KernelInterpolation2D : public Interpolation2D{
      public:
        /*! \pre the \f$ x \f$ values must be sorted.
            \pre kernel needs a Real operator()(Real x) implementation
        */
        template <class I1, class I2, class M, class Kernel>
        KernelInterpolation2D(const I1& xBegin, const I1& xEnd,
                            const I2& yBegin, const I2& yEnd,
                            const M& zData,
                            const Kernel& kernel) {

            impl_ = ext::shared_ptr<Interpolation2D::Impl>(new
                detail::KernelInterpolation2DImpl<I1,I2,M,Kernel>(xBegin, xEnd,
                                                                  yBegin, yEnd,
                                                                  zData, kernel));
            this->update();
        }
    };
}

#endif