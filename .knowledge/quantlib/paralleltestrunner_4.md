eturn boost::exit_exception_failure;
    }
    catch( framework::nothing_to_test const& ) {
        return boost::exit_success;
    }
    catch( framework::internal_error const& ex ) {
        results_reporter::get_stream()
            << "Boost.Test framework internal error: "
            << ex.what() << std::endl;

        return boost::exit_exception_failure;
    }
    catch( framework::setup_error const& ex ) {
        results_reporter::get_stream() << "Test setup error: "
            << ex.what() << std::endl;

        return boost::exit_exception_failure;
    }
    catch( ... ) {
        results_reporter::get_stream()
            << "Boost.Test framework internal error: unknown reason"
            << std::endl;

        return boost::exit_exception_failure;
    }

    framework::shutdown();

    #if BOOST_VERSION < 106000
    return runtime_config::no_result_code()
    #elif BOOST_VERSION < 106400
    // changed in Boost 1.60
    return !runtime_config::get<bool>( runtime_config::RESULT_CODE )
    #else
    // changed again in Boost 1.64
    return !runtime_config::get<bool>( runtime_config::btrt_result_code )
    #endif
        ? boost::exit_success
        : results_collector.results(
            framework::master_test_suite().p_id ).result_code();
}

#endif
