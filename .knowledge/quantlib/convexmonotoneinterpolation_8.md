                           Real b2 = (1.0 + monotonicity_)/2.0;
                            if (eta < b2) {
                                convMonotoneHelper =
                                    ext::shared_ptr<SectionHelper>(
                                        new ConvexMonotone2Helper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           eta, primitive));
                            } else {
                                if (forcePositive_) {
                                    convMonotoneHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new ConvexMonotone4MinHelper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           b2, primitive));
                                } else {
                                    convMonotoneHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new ConvexMonotone4Helper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           b2, primitive));
                                }
                            }
                        }
                        else if ( (gPrev > 0.0 && gNext < 0.0 && gNext > -0.5*gPrev) ||
                                  (gPrev < 0.0 && gNext > 0.0 && gNext < -0.5*gPrev) ) {
                            Real eta = gNext/(gNext-gPrev) * 3.0;
                            Real b3 = (1.0 - monotonicity_)/2.0;
                            if (eta > b3) {
                                convMonotoneHelper =
                                    ext::shared_ptr<SectionHelper>(
                                        new ConvexMonotone3Helper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           eta, primitive));
                            } else {
                                if (forcePositive_) {
                                    convMonotoneHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new ConvexMonotone4MinHelper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           b3, primitive));
                                } else {
                                    convMonotoneHelper =
                                        ext::shared_ptr<SectionHelper>(
                                            new ConvexMonotone4Helper(
                                                           this->xBegin_[i-1],
             