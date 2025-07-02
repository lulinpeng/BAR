load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
def _blst_impl(ctx):
    http_archive(
    name = "com_github_blst",
    urls = ["https://github.com/supranational/blst/archive/refs/tags/v0.3.14.tar.gz"],
    build_file_content = """
genrule(
    name = "build",
    srcs = glob(["**"]),
    outs = ["libblst.a", "blst.h", "blst_aux.h"],
    cmd = '''pwd && ls -al && cd external/*blst*com_github_blst/blst-0.3.14 && ls -al && 
             chmod +x build.sh && ./build.sh && ls -al && pwd && echo $(@D) && 
             cd ../../../ && cp external/*blst*com_github_blst/blst-0.3.14/libblst.a $(@D) && ls -al $(@D) && 
             cp external/*blst*com_github_blst/blst-0.3.14/bindings/*.h $(@D) && ls -al $(@D)''',
)
cc_library(
    name = "blst",
    srcs = ["libblst.a"],
    hdrs = ["blst.h", "blst_aux.h"],
    visibility = ["//visibility:public"],
)
""",
    )
blst = module_extension(
    implementation = _blst_impl
)
