FixedFirstVolatility() :
                                                               fixParameters);
        }

        void calibrate(const std::vector<ext::shared_ptr<BlackCalibrationHelper> >& helpers,
                       OptimizationMethod& method,
                       const EndCriteria& endCriteria,
                       const Constraint& constraint = Constraint(),
                       const std::vector<Real>& weights = std::vector<Real>(),
                       const std::vector<bool>& fixParameters = std::vector<bool>()) {

            std::vector<ext::shared_ptr<CalibrationHelper> > tmp(helpers.size());
            for (Size i=0; i<helpers.size(); ++i)
                tmp[i] = ext::static_pointer_cast<CalibrationHelper>(helpers[i]);

            calibrate(tmp, method, endCriteria, constraint, weights, fixParameters);
        }

        void update() override { LazyObject::update(); }

        // returns the indices of the af region from the last smile update
        std::vector<std::pair<Size, Size> > arbitrageIndices() const {
            calculate();
            return arbitrageIndices_;
        }

        // forces the indices of the af region (useful for sensitivity calculation)
        // if an empty vector is given, the dynamic calculation is used again
        void forceArbitrageIndices(const std::vector<std::pair<Size,Size> >& indices) {
            forcedArbitrageIndices_ = indices;
            this->update();
        }

      protected:
        Real numeraireImpl(Time t, Real y, const Handle<YieldTermStructure>& yts) const override;

        Real
        zerobondImpl(Time T, Time t, Real y, const Handle<YieldTermStructure>& yts) const override;

        void generateArguments() override {
            ext::static_pointer_cast<MfStateProcess>(stateProcess_)->setVols(sigma_.params());
            if(isCalculated())
                updateNumeraireTabulation();
            else
                calculate();
            notifyObservers();
        }

        void performCalculations() const override {
            Gaussian1dModel::performCalculations();
            updateTimes();
            updateSmiles();
            updateNumeraireTabulation();
        }

        std::vector<bool> FixedFirstVolatility() const {
            std::vector<bool> c(volatilities_.size(), false);
            c[0] = true;
            return c;
        }

      private:

        void initialize();
        void updateTimes() const;
        void updateTimes1() const;
        void updateTimes2() const;

        void updateSmiles() const;
        void updateNumeraireTabulation() const;

        void makeSwaptionCalibrationPoint(const Date &expiry,
                                          const Period &tenor);
        void makeCapletCalibrationPoint(const Date &expiry);

        Real marketSwapRate(const Date& expiry,
                            const CalibrationPoint& p,
                            Real digitalPrice,
                            Real guess = 0.03,
                            Real shift = 0.0) const;
        Real marketDigitalPrice(const Date& expiry,
                                const CalibrationPoint& p,
                                const Option::Type& type,
                                Real strike) const;

        Array deflatedZerobondArray(Time T, Time t, const Array& y) const;
        Array numeraireArray(Time t, const Array& y) const;
        Array zerobondArray(Time T, Time t, const Array& y) const;

        Real deflatedZerobond(Time T, Time t = 0.0, Real y = 0.0) const;

        // the following methods (tagged internal) are indended only to produce
        // the volatility diagnostics in the model outputs
        // due to the special convention of the instruments used for numeraire
        // calibration there is on direct way to use the usual pricing engines
        // for this purpose

        Real forwardRateInternal(
            const Date& fixing,
            const Date& referenceDate = Date
