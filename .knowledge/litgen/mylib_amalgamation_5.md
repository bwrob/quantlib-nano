      virtual ~Animal() = default;
    };

    struct Dog : Animal
    {
        MY_API Dog(const std::string &name) : Animal(name + "_dog") { }
        MY_API virtual std::string bark() const { return "BIG WOOF!"; }

        virtual ~Dog() = default;
    };

}

// pybind11 supports bindings for multiple inheritance, nanobind does not
#ifdef BINDING_MULTIPLE_INHERITANCE
namespace Home
{
    struct Pet
    {
        MY_API bool is_pet() const { return true; }
    };

    struct PetDog: public Animals::Dog, public Pet
    {
        MY_API PetDog(const std::string &name): Animals::Dog(name), Pet() {}
        MY_API virtual std::string bark() const { return "woof"; }

        virtual ~PetDog() = default;
    };
}
#endif

MY_API bool binding_multiple_inheritance()
{
#ifdef BINDING_MULTIPLE_INHERITANCE
    return true;
#else
    return false;
#endif
}

// Test that downcasting works: the return type is Animal, but it should bark!
MY_API std::unique_ptr<Animals::Animal> make_dog()
{
    return std::make_unique<Animals::Dog>("Rolf");
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/class_adapt_test.h included by mylib/mylib_main/mylib.h                          //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <cstddef>
#include <cstdint>

struct Color4
{
    // The constructor params will automatically be "adapted" into std::array<uint8_t, 4>
    MY_API Color4(const uint8_t _rgba[4])
    {
        for (size_t i = 0; i < 4; ++i)
            rgba[i] = _rgba[i];
    }

    // This member will be stored as a modifiable numpy array
    uint8_t rgba[4];
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/class_copy_test.h included by mylib/mylib_main/mylib.h                           //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


struct Copyable_ImplicitCopyCtor
{
    int a = 1;
};


struct Copyable_ExplicitCopyCtor
{
    Copyable_ExplicitCopyCtor() = default;
    Copyable_ExplicitCopyCtor(const Copyable_ExplicitCopyCtor& other): a(other.a){}
    int a = 1;
};


struct Copyable_ExplicitPrivateCopyCtor
{
    Copyable_ExplicitPrivateCopyCtor() = default;
    int a = 1;

private:
    Copyable_ExplicitPrivateCopyCtor(const Copyable_ExplicitPrivateCopyCtor& other): a(other.a){}
};


struct Copyable_DeletedCopyCtor
{
    int a = 1;
    Copyable_DeletedCopyCtor() = default;
    Copyable_DeletedCopyCtor(const Copyable_DeletedCopyCtor&) = delete;
};


namespace AAA
{
    template<typename T>
    struct Copyable_Template
    {
        T value;
    };
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/class_virtual_test.h included by mylib/mylib_main/mylib.h                        //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


/*
This test will exercise the following options:

    # class_expose_protected_methods__regex:
    # regex giving the list of class names for which we want to expose protected methods.
    # (by default, only public methods are exposed)
    # If set, this will use the technique described at
    # https://pybind11.readthedocs.io/en/stable/advanced/classes.html#binding-protected-member-functions)
    class_expose_protected_methods__regex: str = ""

    # class_expose_protected_methods__regex:
    # regex giving the list of class names for which we want to be able to override virtual methods
    # from python.
    # (by default, this is not possible)
    # If set, this will use the technique described at
    # https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python
    #
  