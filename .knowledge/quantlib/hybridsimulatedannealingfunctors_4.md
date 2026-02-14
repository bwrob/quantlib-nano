          for (Size i = 0; i < N_; i++) {
                  bounded_[i] = upper[i] - lower[i];
              }
          }
      }
        void setProblem(Problem &P) { problem_ = &P; };
        void operator()(Array & steps, const Array &currentPoint,
            Real currentValue, const Array & currTemp) {
            QL_REQUIRE(currTemp.size() == N_, "Incompatible input");
            QL_REQUIRE(steps.size() == N_, "Incompatible input");

            Array finiteDiffs(N_, 0.0);
            Real finiteDiffMax = 0.0;
            Array ofssetPoint(currentPoint);
            for (Size i = 0; i < N_; i++) {
                ofssetPoint[i] += stepSize_;
                finiteDiffs[i] = bounded_[i] * std::abs((problem_->value(ofssetPoint) - currentValue) / stepSize_);
                ofssetPoint[i] -= stepSize_;
                if (finiteDiffs[i] < minSize_)
                    finiteDiffs[i] = minSize_;
                if (finiteDiffs[i] > finiteDiffMax)
                    finiteDiffMax = finiteDiffs[i];
            }
            for (Size i = 0; i < N_; i++) {
                Real tRatio = initialTemp_[i] / currTemp[i];
                Real sRatio = finiteDiffMax / finiteDiffs[i];
                if (sRatio*tRatio < functionTol_)
                    steps[i] = std::pow(std::fabs(std::log(functionTol_)),
                                        Integer(N_));
                else
                    steps[i] = std::pow(std::fabs(std::log(sRatio*tRatio)),
                                        Integer(N_));
            }
        }
    private:
        Problem *problem_;
        Real stepSize_, minSize_, functionTol_;
        Size N_;
        bool bound_ = false;
        Array lower_, upper_, initialTemp_, bounded_;
    };
}
#endif // HYBRIDSIMULATEDANNEALINGFUNCTORS_H