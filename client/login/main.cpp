#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QScreen>
#include <QDebug>
#include <QTimer>

class LoginWindow : public QWidget {
    Q_OBJECT

public:
    LoginWindow(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::WindowTransparentForInput);

        setStyleSheet("background-color: white;");

        QLabel *emailLabel = new QLabel("Email:", this);
        emailInput = new QLineEdit(this);
        emailInput->setPlaceholderText("Enter your email");

        QLabel *passwordLabel = new QLabel("Password:", this);
        passwordInput = new QLineEdit(this);
        passwordInput->setPlaceholderText("Enter your password");
        passwordInput->setEchoMode(QLineEdit::Password);

        QPushButton *loginButton = new QPushButton("Login", this);
        connect(loginButton, &QPushButton::clicked, this, &LoginWindow::onLoginClicked);

        QVBoxLayout *formLayout = new QVBoxLayout;
        formLayout->addWidget(emailLabel);
        formLayout->addWidget(emailInput);
        formLayout->addWidget(passwordLabel);
        formLayout->addWidget(passwordInput);
        formLayout->addWidget(loginButton);
        formLayout->setSpacing(10);
        formLayout->setContentsMargins(20, 20, 20, 20); 

        QWidget *formContainer = new QWidget(this);
        formContainer->setLayout(formLayout);
        formContainer->setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;");

        QVBoxLayout *mainLayout = new QVBoxLayout;
        mainLayout->addWidget(formContainer);
        mainLayout->setAlignment(Qt::AlignCenter); 
        setLayout(mainLayout);

        formContainer->setFixedSize(300, 200);

        QScreen *screen = QApplication::primaryScreen();
        QRect screenGeometry = screen->availableGeometry();
        setGeometry(screenGeometry);

        showFullScreen();

        QTimer::singleShot(0, this, &LoginWindow::ensureWindowOnTop);
    }

private slots:
    void onLoginClicked() {
        QString email = emailInput->text();
        QString password = passwordInput->text();
        qDebug() << "Email:" << email;
        qDebug() << "Password:" << password;
    }

    void ensureWindowOnTop() {
        setWindowFlags(windowFlags() | Qt::WindowStaysOnTopHint);
        show(); 
    }

private:
    QLineEdit *emailInput;
    QLineEdit *passwordInput;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    LoginWindow loginWindow;
    loginWindow.show();

    return app.exec();
}

#include "main.moc"
