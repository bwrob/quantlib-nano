i) {
                Real gPrev = f[i-1] - this->yBegin_[i];
                Real gNext = f[i] - this->yBegin_[i];
                //first deal with the zero gradient case
                if ( std::fabs(gPrev) < 1.0E-14
                     && std::fabs(gNext) < 1.0E-14 ) {
                    ext::shared_ptr<SectionHelper> singleHelper(
                                     new ConstantGradHelper(f[i-1], primitive,
                                                            this->xBegin_[i-1],
                                                            this->xBegin_[i],
                                                            f[i]));
                    sectionHelpers_[this->xBegin_[i]] = singleHelper;
                } else {
                    Real quadraticity = quadraticity_;
                    ext::shared_ptr<SectionHelper> quadraticHelper;
                    ext::shared_ptr<SectionHelper> convMonotoneHelper;
                    if (quadraticity_ > 0.0) {
                        if (gPrev >= -2.0*gNext && gPrev > -0.5*gNext && forcePositive_) {
                            quadraticHelper =
                                ext::shared_ptr<SectionHelper>(
                                    new QuadraticMinHelper(this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           f[i-1], f[i],
                                                           this->yBegin_[i],
                                                           primitive) );
                        } else {
                            quadraticHelper =
                                ext::shared_ptr<SectionHelper>(
                                    new QuadraticHelper(this->xBegin_[i-1],
                                                        this->xBegin_[i],
                                                        f[i-1], f[i],
                                                        this->yBegin_[i],
                                                        primitive) );
                        }
                    }
                    if (quadraticity_ < 1.0) {

                        if ((gPrev > 0.0 && -0.5*gPrev >= gNext && gNext >= -2.0*gPrev) ||
                            (gPrev < 0.0 && -0.5*gPrev <= gNext && gNext <= -2.0*gPrev)) {
                            quadraticity = 1.0;
                            if (quadraticity_ == 0) {
                                if (forcePositive_) {
                                    quadraticHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new QuadraticMinHelper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           f[i-1], f[i],
                                                           this->yBegin_[i],
                                                           primitive) );
                                } else {
                                    quadraticHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new QuadraticHelper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           f[i-1], f[i],
                                                           this->yBegin_[i],
                                                           primitive) );
                                }
                            }
                        }
                        else if ( (gPrev < 0.0 && gNext > -2.0*gPrev) ||
                                  (gPrev > 0.0 && gNext < -2.0*gPrev)) {

                            Real eta = (gNext + 2.0*gPrev)/(gNext - gPrev);
 