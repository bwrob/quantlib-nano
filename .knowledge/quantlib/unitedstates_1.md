   <li>New Year's Day, January 1st (possibly moved to Monday if
            actually on Sunday)</li>
        <li>Martin Luther King's birthday, third Monday in January (since
            1983)</li>
        <li>Presidents' Day (a.k.a. Washington's birthday),
            third Monday in February</li>
        <li>Good Friday</li>
        <li>Memorial Day, last Monday in May</li>
        <li>Independence Day, July 4th (moved to Monday if Sunday or
            Friday if Saturday)</li>
        <li>Labor Day, first Monday in September</li>
        <li>Columbus Day, second Monday in October</li>
        <li>Veterans' Day, November 11th (moved to Monday if Sunday or
            Friday if Saturday)</li>
        <li>Thanksgiving Day, fourth Thursday in November</li>
        <li>Christmas, December 25th (moved to Monday if Sunday or Friday
            if Saturday)</li>
        </ul>

        Holidays for the North American Energy Reliability Council
        (data from http://www.nerc.com/~oc/offpeaks.html):
        <ul>
        <li>Saturdays</li>
        <li>Sundays</li>
        <li>New Year's Day, January 1st (possibly moved to Monday if
            actually on Sunday)</li>
        <li>Memorial Day, last Monday in May</li>
        <li>Independence Day, July 4th (moved to Monday if Sunday)</li>
        <li>Labor Day, first Monday in September</li>
        <li>Thanksgiving Day, fourth Thursday in November</li>
        <li>Christmas, December 25th (moved to Monday if Sunday)</li>
        </ul>

        Holidays for the Federal Reserve Bankwire System
        (data from https://www.federalreserve.gov/aboutthefed/k8.htm
        and https://www.frbservices.org/about/holiday-schedules):
         <ul>
        <li>Saturdays</li>
        <li>Sundays</li>
        <li>New Year's Day, January 1st (possibly moved to Monday if
            actually on Sunday)</li>
        <li>Martin Luther King's birthday, third Monday in January (since
            1983)</li>
        <li>Presidents' Day (a.k.a. Washington's birthday),
            third Monday in February</li>
        <li>Memorial Day, last Monday in May</li>
        <li>Juneteenth, June 19th (moved to Monday if Sunday)</li>
        <li>Independence Day, July 4th (moved to Monday if Sunday)</li>
        <li>Labor Day, first Monday in September</li>
        <li>Columbus Day, second Monday in October</li>
        <li>Veterans' Day, November 11th (moved to Monday if Sunday)</li>
        <li>Thanksgiving Day, fourth Thursday in November</li>
        <li>Christmas, December 25th (moved to Monday if Sunday)</li>
        </ul>

        \ingroup calendars

        \test the correctness of the returned results is tested
              against a list of known holidays.
    */
    class UnitedStates : public Calendar {
      private:
        class SettlementImpl : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "US settlement"; }
            bool isBusinessDay(const Date&) const override;
        };
        class LiborImpactImpl final : public SettlementImpl {
          public:
            std::string name() const override { return "US with Libor impact"; }
            bool isBusinessDay(const Date&) const override;
        };
        class NyseImpl final : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "New York stock exchange"; }
            bool isBusinessDay(const Date&) const override;
        };
        class GovernmentBondImpl : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "US government bond market"; }
            bool isBusinessDay(const Date&) const override;
        };
        class SofrImpl final : public GovernmentBondImpl {
          public:
            std::string name() const override { return "SOFR fixing calendar"; }
            bool isBusinessDay(const Date&) const override;
        };
        class NercImpl final : public Calen