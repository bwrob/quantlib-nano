a_ + db_*t)*std::exp(-c_*t);
        return t<0 ? 0.0 : Real((da_ + db_*t)*std::exp(-c_*t));
    }

    inline Real AbcdMathFunction::primitive(Time t) const {
        //return (pa_ + pb_*t)*std::exp(-c_*t) + d_*t + K_;
        return t<0 ? 0.0 : Real((pa_ + pb_*t)*std::exp(-c_*t) + d_*t + K_);
    }

    inline Real AbcdMathFunction::maximumValue() const {
        if (b_==0.0 || a_<=0.0)
            return d_;
        return (*this)(maximumLocation());
    }

}

#endif