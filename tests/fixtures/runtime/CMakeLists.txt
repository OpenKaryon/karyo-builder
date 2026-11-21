cmake_minimum_required(VERSION 3.21)
project(KaryoRuntimeFixture LANGUAGES CXX)
include(CTest)
include(GNUInstallDirs)
find_package(Qt6 6.4 REQUIRED COMPONENTS Core)
add_executable(runtime-fixture main.cpp)
target_link_libraries(runtime-fixture PRIVATE Qt6::Core)
install(TARGETS runtime-fixture RUNTIME DESTINATION bin COMPONENT runtime)
add_test(NAME runtime-fixture COMMAND runtime-fixture)

install(FILES example.conf DESTINATION ${CMAKE_INSTALL_SYSCONFDIR}/karyo-builder-runtime-check COMPONENT runtime)

install(FILES example.conf DESTINATION share/doc/karyo-builder-runtime-doc COMPONENT documentation)
