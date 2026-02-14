 copy_size);
        free(m_start);

        m_start = tmp;
        m_end = m_start + new_alloc_size;
        m_cur = m_start + used_size;
    }

private:
    char *m_start{nullptr}, *m_cur{nullptr}, *m_end{nullptr};
};

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
