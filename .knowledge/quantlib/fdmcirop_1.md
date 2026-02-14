ize direction, const Array& r, Real s) const override;
        Array preconditioner(const Array& r, Real s) const override;

        std::vector<SparseMatrix> toMatrixDecomp() const override;

      private:
        FdmCIREquityPart dxMap_;
        FdmCIRRatesPart dyMap_;
        FdmCIRMixedPart dzMap_;
    };
}

#endif
