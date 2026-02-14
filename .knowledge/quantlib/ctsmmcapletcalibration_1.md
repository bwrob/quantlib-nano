  
        ext::shared_ptr<CurveState> cs_;
        Spread displacement_;
        Size numberOfRates_;
        // working variables
        std::vector<Volatility> usedCapletVols_;
        // results
        bool calibrated_;
        Natural failures_;
        Real deformationSize_;
        Real capletRmsError_, capletMaxError_;
        Real swaptionRmsError_, swaptionMaxError_;
        std::vector<Matrix> swapCovariancePseudoRoots_;
    };

    // inline

    inline const std::vector<Volatility>&
    CTSMMCapletCalibration::mktCapletVols() const {
        return mktCapletVols_;
    }

    inline const std::vector<Volatility>&
    CTSMMCapletCalibration::mdlCapletVols() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return mdlCapletVols_;
    }

    inline const std::vector<Volatility>&
    CTSMMCapletCalibration::mktSwaptionVols() const {
        return mktSwaptionVols_;
    }

    inline const std::vector<Volatility>&
    CTSMMCapletCalibration::mdlSwaptionVols() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return mdlSwaptionVols_;
    }

    inline Natural CTSMMCapletCalibration::failures() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return failures_;
    }

    inline Real CTSMMCapletCalibration::deformationSize() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return deformationSize_;
    }

    inline Real CTSMMCapletCalibration::capletRmsError() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return capletRmsError_;
    }

    inline Real CTSMMCapletCalibration::capletMaxError() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return capletMaxError_;
    }

    inline Real CTSMMCapletCalibration::swaptionRmsError() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return swaptionRmsError_;
    }

    inline Real CTSMMCapletCalibration::swaptionMaxError() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return swaptionMaxError_;
    }

    inline const std::vector<Matrix>&
    CTSMMCapletCalibration::swapPseudoRoots() const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        return swapCovariancePseudoRoots_;
    }

    inline const Matrix&
    CTSMMCapletCalibration::swapPseudoRoot(Size i) const {
        QL_REQUIRE(calibrated_, "not successfully calibrated yet");
        QL_REQUIRE(i<swapCovariancePseudoRoots_.size(),
                   i << "is an invalid index, must be less than "
                   << swapCovariancePseudoRoots_.size());
        return swapCovariancePseudoRoots_[i];
    }

    inline const ext::shared_ptr<CurveState>&
    CTSMMCapletCalibration::curveState() const {
        return cs_;
    }

    inline std::vector<Spread>
    CTSMMCapletCalibration::displacements() const {
        return std::vector<Volatility>(numberOfRates_, displacement_);
    }

}

#endif