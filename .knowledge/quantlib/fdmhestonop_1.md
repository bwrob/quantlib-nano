      Array apply_direction(Size direction, const Array& r) const override;
        Array solve_splitting(Size direction, const Array& r, Real s) const override;
        Array preconditioner(const Array& r, Real s) const override;

        std::vector<SparseMatrix> toMatrixDecomp() const override;

      private:
        NinePointLinearOp correlationMap_;
        FdmHestonVariancePart dyMap_;
        FdmHestonEquityPart dxMap_;
    };
}

#endif
