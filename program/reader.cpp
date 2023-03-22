#include <QtCore/QCoreApplication>
#include <QTextStream>
#include <QMessageBox>
#include <QApplication>
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QMessageBox::information(NULL, "Hello", "Hello", "Ok");
    return a.exec();
}
