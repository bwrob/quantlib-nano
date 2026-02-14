# Headers amalgamation

Litgen processes files individually, and if a subclass is defined in a different file than its parent, inherited members may not be correctly bound.
Sometimes it is worthwhile to first generate an `Amalgamation Header` for a library before generating bindings for it.
An amalgamation header is a single header file that includes all the public headers of a library.

## Amalgamation utility

`litgen` provides a utility function `write_amalgamate_header_file` to generate an Amalgamation header file.
It is available in the `codemanip.amalgamated_header` module.

```python
from codemanip import amalgamated_header
```

And its API is as follows:
```python
@dataclass
class AmalgamationOptions:
    base_dir: str                     # The base directory of the headers
    local_includes_startwith: str     # Only headers whose name begin with this string should be included
    include_subdirs: list[str]        # Include only headers in these subdirectories

    main_header_file: str             # The main header file
    dst_amalgamated_header_file: str  # The destination file

def write_amalgamate_header_file(options: AmalgamationOptions) -> None:
    ...
```

`write_amalgamate_header_file` takes an `AmalgamationOptions` object as an argument and generates an Amalgamation header file.
It will include all the headers whose name starts with `local_includes_startwith` in the `base_dir` directory
and its subdirectories given in `include_subdirs`.

Note: it will include any file only once: if a file was already included by another file, it will not be included again.
