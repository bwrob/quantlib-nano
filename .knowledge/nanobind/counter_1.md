#  define NAMESPACE_END(name) }
#endif

NAMESPACE_BEGIN(nanobind)

/** \brief Simple intrusive reference counter.
 *
 * Intrusive reference counting is a simple solution for various lifetime and
 * ownership-related issues that can arise in Python bindings of C++ code. The
 * implementation here represents one of many ways in which intrusive reference
 * counting can be realized and is included for convenience.
 *
 * The ``intrusive_counter`` class represents an atomic counter that can be
 * increased (via ``inc_ref()``) or decreased (via ``dec_ref()``). When the
 * counter reaches zero, the object should be deleted, which ``dec_ref()``
 * indicates by returning ``true``.
 *
 * In addition to this simple counting mechanism, ownership of the object can
 * also be transferred to Python (via ``set_self_py()``). In this case,
 * subsequent calls to ``inc_ref()`` and ``dec_ref()`` modify the reference
 * count of the underlying Python object. The ``intrusive_counter`` class
 * supports both cases using only ``sizeof(void*)`` bytes of storage.
 *
 * To incorporate intrusive reference counting into your own project, you would
 * usually add an ``intrusive_counter``-typed member to the base class of an
 * object hierarchy and expose it as follows:
 *
 * ```cpp
 * #include <nanobind/intrusive/counter.h>
 *
 * class Object {
 * public:
 *     void inc_ref() noexcept { m_ref_count.inc_ref(); }
 *     bool dec_ref() noexcept { return m_ref_count.dec_ref(); }
 *
 *     // Important: must declare virtual destructor
 *     virtual ~Object() = default;
 *
 *     void set_self_py(PyObject *self) noexcept {
 *         m_ref_count.set_self_py(self);
 *     }
 *
 * private:
 *     nb::intrusive_counter m_ref_count;
 * };
 *
 * // Convenience function for increasing the reference count of an instance
 * inline void inc_ref(Object *o) noexcept {
 *     if (o)
 *        o->inc_ref();
 * }
 *
 * // Convenience function for decreasing the reference count of an instance
 * // and potentially deleting it when the count reaches zero
 * inline void dec_ref(Object *o) noexcept {
 *     if (o && o->dec_ref())
 *         delete o;
 * }
 * ```
 *
 * Alternatively, you could also inherit from ``intrusive_base``, which obviates
 * the need for all of the above declarations:
 *
 * ```cpp
 * class Object : public intrusive_base {
 * public:
 *     // ...
 * };
 * ```
 *
 * When binding the base class in Python, you must indicate to nanobind that
 * this type uses intrusive reference counting and expose the ``set_self_py``
 * member. This must only be done once, as the attribute is automatically
 * inherited by subclasses.
 *
 * ```cpp
 * nb::class_<Object>(
 *   m, "Object",
 *   nb::intrusive_ptr<Object>(
 *       [](Object *o, PyObject *po) noexcept { o->set_self_py(po); }));
 * ```
 *
 * Also, somewhere in your binding initialization code, you must call
 *
 * ```cpp
 * nb::intrusive_init(
 *     [](PyObject *o) noexcept {
 *         nb::gil_scoped_acquire guard;
 *         Py_INCREF(o);
 *     },
 *     [](PyObject *o) noexcept {
 *         nb::gil_scoped_acquire guard;
 *         Py_DECREF(o);
 *     });
 * ```
 *
 * For this all to compile, a single one of your .cpp files must include this
 * header file from somewhere as follows:
 *
 * ```cpp
 * #include <nanobind/intrusive/counter.inl>
 * ```
 *
 * Calling the ``inc_ref()`` and ``dec_ref()`` members many times throughout
 * the code can quickly become tedious. Nanobind also ships with a ``ref<T>``
 * RAII helper class to help with this.
 *
 * ```cpp
 * #include <nanobind/intrusive/ref.h>
 *
 * {
 *     ref<MyObject> x = new MyObject(); // <-- assigment to ref<..> automatically calls inc_ref()
 *     x->func(); // ref<..> can be used like a normal pointer
 * } // <-- Destruction of ref<..> calls dec_ref(), deleting the instance in this example.
 * ```
 *
 * When the file ``nanobind/intrusive/ref.h`` is included following
 * ``nanobind/nanobind.h``, it also exposes a custom type caster to bind
 * functions t