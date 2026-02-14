line Natural Bond::settlementDays() const {
        return settlementDays_;
    }

    inline const Calendar& Bond::calendar() const {
        return calendar_;
    }

    inline const std::vector<Real>& Bond::notionals() const {
        return notionals_;
    }

    inline const Leg& Bond::cashflows() const {
        return cashflows_;
    }

    inline const Leg& Bond::redemptions() const {
        return redemptions_;
    }

    inline Date Bond::issueDate() const {
        return issueDate_;
    }

}

#endif