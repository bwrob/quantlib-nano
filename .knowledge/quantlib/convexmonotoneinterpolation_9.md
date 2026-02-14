                                              this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           b3, primitive));
                                }
                            }
                        } else {
                            Real eta = gNext/(gPrev + gNext);
                            Real b2 = (1.0 + monotonicity_)/2.0;
                            Real b3 = (1.0 - monotonicity_)/2.0;
                            if (eta > b2)
                                eta = b2;
                            if (eta < b3)
                                eta = b3;
                            if (forcePositive_) {
                                convMonotoneHelper =
                                    ext::shared_ptr<SectionHelper>(
                                        new ConvexMonotone4MinHelper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           eta, primitive));
                            } else {
                                convMonotoneHelper =
                                    ext::shared_ptr<SectionHelper>(
                                        new ConvexMonotone4Helper(
                                                           this->xBegin_[i-1],
                                                           this->xBegin_[i],
                                                           gPrev, gNext,
                                                           this->yBegin_[i],
                                                           eta, primitive));
                            }
                        }
                    }

                    if (quadraticity == 1.0) {
                        sectionHelpers_[this->xBegin_[i]] = quadraticHelper;
                    } else if (quadraticity == 0.0) {
                        sectionHelpers_[this->xBegin_[i]] = convMonotoneHelper;
                    } else {
                        sectionHelpers_[this->xBegin_[i]] =
                            ext::shared_ptr<SectionHelper>(
                                           new ComboHelper(quadraticHelper,
                                                           convMonotoneHelper,
                                                           quadraticity));
                    }

                }
                primitive +=
                    this->yBegin_[i] * (this->xBegin_[i]-this->xBegin_[i-1]);
            }

            if (constantLastPeriod_) {
                sectionHelpers_[this->xBegin_[length_-1]] =
                    ext::shared_ptr<SectionHelper>(
                        new EverywhereConstantHelper(this->yBegin_[length_-1],
                                                     primitive,
                                                     this->xBegin_[length_-2]));
                extrapolationHelper_ = sectionHelpers_[this->xBegin_[length_-1]];
            } else {
                extrapolationHelper_ =
                    ext::shared_ptr<SectionHelper>(
                        new EverywhereConstantHelper(
                                (sectionHelpers_.rbegin())->second->value(*(this->xEnd_-1)),
                                primitive,
                                *(this->xEnd_-1)));
            }
        }

        template <class I1, class I2>
        Real ConvexMonotoneImpl<I1,I2>::value(Real x) const {
            if (x >= *(this->xEnd_-1)) {
                return extrapolationHelper_->value(x);
            }

            return sectionHelpers_.upper_bound(x)->second->value(x);
        }

        templat