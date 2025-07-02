load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
def _c_kzg_4844_impl(ctx):
    http_archive(
    name = "com_github_c_kzg_4844",
    urls = ["https://github.com/ethereum/c-kzg-4844/archive/refs/tags/v2.1.1.tar.gz"],
    strip_prefix = "c-kzg-4844-2.1.1",
    build_file_content = """
cc_library(
    name = "ckzg",
    srcs = glob(["src/*.c", "src/**/*.c"]),
    textual_hdrs = glob(["src/**/*.c"]),
    hdrs = glob(["src/*.h", "src/**/*.h", "bindings/**/*.h"]),
    includes = ["src", "src/common", "src/eip4844", "src/eip7594", "src/setup"],
    deps = ["@com_github_blst//:blst"],
    linkstatic = True,
    visibility = ["//visibility:public"],
)
    """,
    )
c_kzg_4844 = module_extension(implementation = _c_kzg_4844_impl)
