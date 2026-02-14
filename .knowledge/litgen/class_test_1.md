 this class!
    // When building the bindings, we need to add MyStructWithNestedEnum::
    MY_API int HandleChoice(Choice value = Choice::A) { return 0; }
};

struct ClassWithInlineForwardDeclaredMethod
{
    MY_API inline int GetTexID();
};

MY_API inline int ClassWithInlineForwardDeclaredMethod::GetTexID()
{
    return 42;
}