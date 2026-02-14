       ValuesFn values_;
    };

    class ParametersTransformation {
      public:
        virtual ~ParametersTransformation() = default;
        virtual Array direct(const Array& x) const = 0;
        virtual Array inverse(const Array& x) const = 0;
    };
}

#endif