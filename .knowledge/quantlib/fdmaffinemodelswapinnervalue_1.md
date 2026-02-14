AffineModelSwapInnerValue<ModelType>::innerValue(
        const FdmLinearOpIterator& iter, Time t) {

        const Date& iterExerciseDate = exerciseDates_.find(t)->second;

        const Array disRate(getState(disModel_, t, iter));
        const Array fwdRate(getState(fwdModel_, t, iter));

        if (disTs_.empty() || iterExerciseDate != disTs_->referenceDate()) {

            const Handle<YieldTermStructure> discount
                = disModel_->termStructure();

            disTs_.linkTo(ext::shared_ptr<YieldTermStructure>(
                new FdmAffineModelTermStructure(disRate,
                    discount->calendar(), discount->dayCounter(),
                    iterExerciseDate, discount->referenceDate(),
                    disModel_)));

            const Handle<YieldTermStructure> fwd = fwdModel_->termStructure();

            fwdTs_.linkTo(ext::shared_ptr<YieldTermStructure>(
                new FdmAffineModelTermStructure(fwdRate,
                    fwd->calendar(), fwd->dayCounter(),
                    iterExerciseDate, fwd->referenceDate(),
                    fwdModel_)));

        }
        else {
            ext::dynamic_pointer_cast<FdmAffineModelTermStructure>(
                disTs_.currentLink())->setVariable(disRate);
            ext::dynamic_pointer_cast<FdmAffineModelTermStructure>(
                fwdTs_.currentLink())->setVariable(fwdRate);
        }

        Real npv = 0.0;
        for (Size j = 0; j < 2; j++) {
            for (const auto& i : swap_->leg(j)) {
                npv +=
                    ext::dynamic_pointer_cast<Coupon>(i)->accrualStartDate() >= iterExerciseDate ?
                        Real(i->amount() * disTs_->discount(i->date())) :
                        0.0;
            }
            if (j == 0)
                npv *= -1.0;
        }
        if (swap_->type() == Swap::Receiver)
            npv *= -1.0;

        return std::max(0.0, npv);
    }

    template <class ModelType> inline
    Real FdmAffineModelSwapInnerValue<ModelType>::avgInnerValue(
        const FdmLinearOpIterator& iter, Time t) {
        return innerValue(iter, t);
    }

}
#endif