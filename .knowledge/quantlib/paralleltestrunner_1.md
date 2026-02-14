TestCaseId {
        test_unit_id id;
        bool terminate;
    };

    struct RuntimeLog {
        QuantLib::Time time;
        char testCaseName[256];
    };

    struct QualifiedTestResults {
        test_unit_id id;
        test_results results;
    };

    const char* const namesLogMutexName = "named_log_mutex";

    void output_logstream(
        std::ostream& out, std::streambuf* outBuf, std::stringstream& s) {

        static named_mutex mutex(open_or_create, namesLogMutexName);
        scoped_lock<named_mutex> lock(mutex);

        out.flush();
        out.rdbuf(outBuf);

        std::vector<std::string> tok;
        const std::string lines = s.str();
        boost::split(tok, lines, boost::is_any_of("\n"));

        for (std::vector<std::string>::const_iterator iter = tok.begin();
            iter != tok.end(); ++iter) {
            if ((iter->length() != 0u) && (iter->compare("Running 1 test case...") != 0)) {
                out << *iter  << std::endl;
            }
        }

        s.str(std::string());
        out.rdbuf(s.rdbuf());
    }

    std::ostream& log_stream() {
    #if BOOST_VERSION < 106200
        return s_log_impl().stream();
    #else
        return s_log_impl().m_log_formatter_data.front().stream();
    #endif
    }
}


test_suite* init_unit_test_suite(int, char* []);

int main( int argc, char* argv[] )
{
    using QuantLib::Time;

    const char* const profileFileName = ".unit_test_profile.txt";
    const char* const testUnitIdQueueName = "test_unit_queue";
    const char* const testResultQueueName = "test_result_queue";
    const char* const testRuntimeLogName  = "test_runtime_log_queue";

    const std::string clientModeStr = "--client_mode=true";
    const bool clientMode = (std::string(argv[argc-1]) == clientModeStr);

    message_queue::size_type recvd_size;

    try {
        unsigned int priority;
        if (!clientMode) {
            std::map<std::string, Time> runTimeLog;

            std::ifstream in(profileFileName);
            if (in.good()) {
                // NOLINTNEXTLINE(readability-implicit-bool-conversion)
                for (std::string line; std::getline(in, line);) {
                    std::vector<std::string> tok;
                    boost::split(tok, line, boost::is_any_of(":"));

                    QL_REQUIRE(tok.size() == 2,
                        "every line should consists of two entries");
                    runTimeLog[tok[0]] = std::stod(tok[1]);
                }
            }
            in.close();

            auto nProc = std::thread::hardware_concurrency();

            std::vector<std::string> workerArgs;
            std::vector<char*> localArgs(1, argv[0]);

            for( int i = 1; i < argc; ++i ) {
                const std::string arg(argv[i]);

                // check for number of processes
                std::vector<std::string> tok;
                boost::split(tok, arg, boost::is_any_of("="));
                if (tok[0] == "--nProc" && tok.size() == 2) {
                    nProc = std::stoul(tok[1]);
                }
                else if (tok[0] != "--build_info") {
                    if (tok[0] != "--run_test")
                        workerArgs.push_back(argv[i]);
                    localArgs.push_back(argv[i]);
                }
            }

            workerArgs.push_back(clientModeStr);

            framework::init(init_unit_test_suite,
                            localArgs.size(), &localArgs[0]);
            framework::finalize_setup_phase();

            framework::impl::s_frk_state().deduce_run_status(
                framework::master_test_suite().p_id);

            TestCaseCollector tcc;
            traverse_test_tree(framework::master_test_suite(), tcc , true);

            log_stream() << "Total number of test cases: "
                << tcc.numberOfTests() << std::endl;

            log_stream() << "Total number of worker processes: "
                << nProc << std::endl;

            message_queue::remove(test
