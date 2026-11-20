// SPDX-License-Identifier: GPL-3.0-or-later
#include <QCoreApplication>
#include <QtGlobal>
#include <iostream>

int main(int argc, char **argv)
{
    QCoreApplication application(argc, argv);
    std::cout << qVersion() << '\n';
    return application.applicationPid() > 0 ? 0 : 1;
}
