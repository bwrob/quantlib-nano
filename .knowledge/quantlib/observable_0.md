/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
Copyright (C) 2011, 2012 Ferdinando Ametrano
Copyright (C) 2013 Chris Higgs
Copyright (C) 2015 Klaus Spanderen


This file is part of QuantLib, a free-software/open-source library
for financial quantitative analysts and developers - http://quantlib.org/

QuantLib is free software: you can redistribute it and/or modify it
under the terms of the QuantLib license.  You should have received a
copy of the license along with this program; if not, please email
<quantlib-dev@lists.sf.net>. The license is also available online at
<https://www.quantlib.org/license.shtml>.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the license for more details.
*/

/*! \file observable.hpp
    \brief observer/observable pattern
*/

#ifndef quantlib_observable_hpp
#define quantlib_observable_hpp

#include <ql/errors.hpp>
#include <ql/patterns/singleton.hpp>
#include <ql/shared_ptr.hpp>
#include <ql/types.hpp>
#include <set>
#include <map>

#if !defined(QL_USE_STD_SHARED_PTR) && BOOST_VERSION < 107400

namespace std {

    template<typename T>
    struct hash<boost::shared_ptr<T>> {
        std::size_t operator()(const boost::shared_ptr<T>& ptr) const noexcept {
            return std::hash<typename boost::shared_ptr<T>::element_type*>()(ptr.get());
        }
    };

}

#endif

#ifndef QL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN

namespace QuantLib {

    class Observer;
    class ObservableSettings;

    //! Object that notifies its changes to a set of observers
    /*! \ingroup patterns */
    class Observable {
        friend class Observer;
        friend class ObservableSettings;
      public:
        // constructors, assignment, destructor
        Observable() = default;
        Observable(const Observable&);
        Observable& operator=(const Observable&);
        // delete the move operations because the semantics are not yet clear
        Observable(Observable&&) = delete;
        Observable& operator=(Observable&&) = delete;
        virtual ~Observable() = default;
        /*! This method should be called at the end of non-const methods
            or when the programmer desires to notify any changes.
        */
        void notifyObservers();
      private:
        typedef std::set<Observer*> set_type;
        typedef set_type::iterator iterator;
        std::pair<iterator, bool> registerObserver(Observer*);
        Size unregisterObserver(Observer*);
        set_type observers_;
    };

    //! global repository for run-time library settings
    class ObservableSettings : public Singleton<ObservableSettings> {
        friend class Singleton<ObservableSettings>;
        friend class Observable;
      public:
        void disableUpdates(bool deferred=false) {
            updatesEnabled_  = false;
            updatesDeferred_ = deferred;
        }
        void enableUpdates();

        bool updatesEnabled() const { return updatesEnabled_; }
        bool updatesDeferred() const { return updatesDeferred_; }
        bool runningDeferredUpdates() const { return runningDeferredUpdates_; }

      private:
        ObservableSettings() = default;

        typedef std::map<Observer*, bool> set_type;
        typedef set_type::iterator iterator;

        void registerDeferredObservers(const Observable::set_type& observers);
        void unregisterDeferredObserver(Observer*);

        set_type deferredObservers_;

        bool updatesEnabled_ = true, updatesDeferred_ = false;
        bool runningDeferredUpdates_ = false;
    };

    //! Object that gets notified when a given observable changes
    /*! \ingroup patterns */
    class Observer { // NOLINT(cppcoreguidelines-special-member-functions)
      private:
        typedef std::set<ex