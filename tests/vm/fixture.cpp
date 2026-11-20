// SPDX-License-Identifier: GPL-3.0-or-later
#include <QApplication>
#include <QDir>
#include <QFile>
#include <QLabel>
#include <QMenu>
#include <QPushButton>
#include <QSystemTrayIcon>
#include <QVBoxLayout>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("qa-tray-fixture"));
    app.setDesktopFileName(QStringLiteral("qa-tray-fixture"));
    app.setQuitOnLastWindowClosed(false);
    QDir::home().mkpath(QStringLiteral("qa-results"));
    const auto record = [](const QByteArray &event) {
        QFile file(QDir::homePath() + QStringLiteral("/qa-results/tray.log"));
        if (file.open(QIODevice::Append))
            file.write(event + '\n');
    };
    QPixmap tile(32, 32);
    tile.fill(QColor(20, 190, 90));
    const QIcon icon(tile);
    app.setWindowIcon(icon);
    QWidget window;
    window.setWindowTitle(QStringLiteral("QA Tray Fixture"));
    window.resize(360, 160);
    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(new QLabel(QStringLiteral("Real Qt status-notifier fixture")));
    auto *hide = new QPushButton(QStringLiteral("Hide window"));
    layout->addWidget(hide);
    QObject::connect(hide, &QPushButton::clicked, &window, &QWidget::hide);
    QSystemTrayIcon tray(icon);
    tray.setToolTip(QStringLiteral("QA Tray Fixture"));
    QMenu menu;
    menu.addAction(QStringLiteral("Open fixture"), [&] { record("menu-open"); window.show(); });
    menu.addAction(QStringLiteral("Quit fixture"), &app, &QApplication::quit);
    tray.setContextMenu(&menu);
    QObject::connect(&tray, &QSystemTrayIcon::activated, &app, [&](QSystemTrayIcon::ActivationReason reason) {
        record("activated-" + QByteArray::number(int(reason)));
        if (reason == QSystemTrayIcon::Trigger || reason == QSystemTrayIcon::DoubleClick) {
            window.show();
            window.raise();
            window.activateWindow();
        }
    });
    tray.show();
    record("started");
    return app.exec();
}
