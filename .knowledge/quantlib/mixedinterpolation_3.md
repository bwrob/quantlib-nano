yBegin_);
                    interpolation2_ = factory2.interpolate(this->xBegin2_,
                                                           this->xEnd_,
                                                           this->yBegin_ + n);
                    break;
                  default:
                    QL_FAIL("unknown mixed-interpolation behavior: " << behavior);
                }
            }

            void update() {
                interpolation1_.update();
                interpolation2_.update();
            }
            Real value(Real x) const {
                if (x<*xBegin2_)
                    return interpolation1_(x, true);
                return interpolation2_(x, true);
            }
            Real primitive(Real x) const {
                if (x<*xBegin2_)
                    return interpolation1_.primitive(x, true);
                return interpolation2_.primitive(x, true) -
                    interpolation2_.primitive(*xBegin2_, true) +
                    interpolation1_.primitive(*xBegin2_, true);
            }
            Real derivative(Real x) const {
                if (x<*xBegin2_)
                    return interpolation1_.derivative(x, true);
                return interpolation2_.derivative(x, true);
            }
            Real secondDerivative(Real x) const {
                if (x<*xBegin2_)
                    return interpolation1_.secondDerivative(x, true);
                return interpolation2_.secondDerivative(x, true);
            }
          private:
            I1 xBegin2_;
            Interpolation interpolation1_, interpolation2_;
        };

    }

}

#endif