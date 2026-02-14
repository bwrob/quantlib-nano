lPart_ = I_ - 0.5*alpha_*dt_*L_;
        }
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyBeforeApplying(explicitTrapezoidalPart_);
        a = explicitTrapezoidalPart_.applyTo(a);
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyAfterApplying(a);

        // trapezoidal implicit part
        if (L_.isTimeDependent()) {
            L_.setTime(t-dt_);
            implicitPart_ = I_ + 0.5*alpha_*dt_*L_;
        }
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyBeforeSolving(implicitPart_,a);
        a = implicitPart_.solveFor(a);
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyAfterSolving(a);


        // BDF2 explicit part
        if (L_.isTimeDependent()) {
            L_.setTime(t);
        }
        for (i=0; i<bcs_.size(); i++) {
            bcs_[i]->applyBeforeApplying(explicitBDF2PartFull_);
        }
        array_type b0 = explicitBDF2PartFull_.applyTo(aInit_);
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyAfterApplying(b0);

        for (i=0; i<bcs_.size(); i++) {
            bcs_[i]->applyBeforeApplying(explicitBDF2PartMid_);
        }
        array_type b1 = explicitBDF2PartMid_.applyTo(a);
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyAfterApplying(b1);
        a = b0+b1;

        // reuse implicit part - works only for alpha=2-sqrt(2)
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyBeforeSolving(implicitPart_,a);
        a = implicitPart_.solveFor(a);
        for (i=0; i<bcs_.size(); i++)
            bcs_[i]->applyAfterSolving(a);

    }

}

#endif