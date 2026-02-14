(dBegin++);
                    invalidValue = *(vBegin++);
                }
            }
            QL_DEPRECATED_DISABLE_WARNING
            notifier(name)->notifyObservers();
            QL_DEPRECATED_ENABLE_WARNING
            QL_REQUIRE(noInvalidFixing, "At least one invalid fixing provided: "
                                            << invalidDate.weekday() << " " << invalidDate << ", "
                                            << invalidValue);
            QL_REQUIRE(noDuplicatedFixing, "At least one duplicated fixing provided: "
                                               << duplicatedDate << ", " << duplicatedValue
                                               << " while " << h[duplicatedDate]
                                               << " value is already present");
        }

        bool hasHistory(const std::string& name) const;
        const TimeSeries<Real>& getHistory(const std::string& name) const;
        void clearHistory(const std::string& name);
        bool hasHistoricalFixing(const std::string& name, const Date& fixingDate) const;
        void setHistory(const std::string& name, TimeSeries<Real> history);
        ext::shared_ptr<Observable> notifier(const std::string& name) const;
    };

}


#endif