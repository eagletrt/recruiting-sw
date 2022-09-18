#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include "data.hpp"

int main(int argc, char *argv[]) {
  QGuiApplication app(argc, argv);

  // Data generator
  Data *data = new Data(&app);

  // You can received data using Qt Signals and Slots.
  // https://doc.qt.io/qt-5/signalsandslots.html

  // example:
  // QObject::connect(data, &Data::dataReceived, backend, &Backend::ingestData);

  QQmlApplicationEngine engine;
  const QUrl url(QStringLiteral("qrc:/main.qml"));
  QObject::connect(
      &engine, &QQmlApplicationEngine::objectCreated, &app,
      [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl) QCoreApplication::exit(-1);
      },
      Qt::QueuedConnection);
  engine.load(url);

  return app.exec();
}
