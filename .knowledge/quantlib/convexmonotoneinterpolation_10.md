e <class I1, class I2>
        Real ConvexMonotoneImpl<I1,I2>::primitive(Real x) const {
            if (x >= *(this->xEnd_-1)) {
                return extrapolationHelper_->primitive(x);
            }

            return sectionHelpers_.upper_bound(x)->second->primitive(x);
        }

    }

}

#endif
