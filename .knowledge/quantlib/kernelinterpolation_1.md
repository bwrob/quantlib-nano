 yVec_);

                for (Real i : diffVec) {
                    QL_REQUIRE(i < invPrec_, "Inversion failed in 1d kernel interpolation");
                }
            }

            Size xSize_;
            Real invPrec_;
            Matrix M_;
            Array alphaVec_,yVec_;
            Kernel kernel_;
        };

    } // end namespace detail


    //! Kernel interpolation between discrete points
    /*! Implementation of the kernel interpolation approach, which can
        be found in "Foreign Exchange Risk" by Hakala, Wystup page
        256.

        The kernel in the implementation is kept general, although a Gaussian
        is considered in the cited text.

        \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class KernelInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted.
            \pre kernel needs a Real operator()(Real x) implementation

            The calculation will solve \f$ y = Ma \f$ for \f$a\f$.
            Due to singularity or rounding errors the recalculation
            \f$ Ma \f$ may not give \f$ y\f$. Here, a failure will
            be thrown if
            \f[
            \left\| Ma-y \right\|_\infty \geq \epsilon
            \f] */
        template <class I1, class I2, class Kernel>
        KernelInterpolation(const I1& xBegin, const I1& xEnd,
                            const I2& yBegin,
                            const Kernel& kernel,
                            const double epsilon = 1.0E-7) {
            impl_ = ext::shared_ptr<Interpolation::Impl>(new
                detail::KernelInterpolationImpl<I1,I2,Kernel>(xBegin, xEnd,
                                                              yBegin, kernel,
                                                              epsilon));
            impl_->update();
        }

    };
}

#endif