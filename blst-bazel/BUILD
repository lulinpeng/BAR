load("@rules_cc//cc:defs.bzl", "cc_binary")
load("@rules_cc//cc:defs.bzl", "cc_proto_library")

cc_binary(
    name = "main",
    srcs = ["main.cpp"],
    deps = [":bar_blst"]
)

cc_library(
    name = "bar_blst",
    deps = ["@com_github_blst//:blst"],
    visibility = ["//visibility:public"]
)
