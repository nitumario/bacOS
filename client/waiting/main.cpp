#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>
#include <QScreen> 

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;

    window.setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);

    window.setStyleSheet("background-color: white;");

    QLabel *label = new QLabel("Se așteaptă începerea evenimentului", &window);
    label->setAlignment(Qt::AlignCenter);
    label->setStyleSheet("font-size: 24px; color: black;");

    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget(label);
    layout->setContentsMargins(0, 0, 0, 0); 
    layout->setSpacing(0); 
    window.setLayout(layout);

    QScreen *screen = QApplication::primaryScreen();
    QRect screenGeometry = screen->availableGeometry();
    
    window.setGeometry(screenGeometry);

    window.showFullScreen();

    return app.exec();
}
