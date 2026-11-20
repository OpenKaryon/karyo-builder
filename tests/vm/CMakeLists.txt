# SPDX-License-Identifier: GPL-3.0-or-later
cmake_minimum_required(VERSION 3.21)
project(KaryoSessionFixture LANGUAGES CXX)
find_package(Qt6 REQUIRED COMPONENTS Widgets)
add_executable(qa-tray-fixture fixture.cpp)
target_link_libraries(qa-tray-fixture PRIVATE Qt6::Widgets)
