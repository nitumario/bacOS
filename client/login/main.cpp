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
        // Set window flags to make it frameless and always on top
        setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::WindowTransparentForInput);

        // Set the window background color to white
        setStyleSheet("background-color: white;");

        // Create UI elements
        QLabel *emailLabel = new QLabel("Email:", this);
        emailInput = new QLineEdit(this);
        emailInput->setPlaceholderText("Enter your email");

        QLabel *passwordLabel = new QLabel("Password:", this);
        passwordInput = new QLineEdit(this);
        passwordInput->setPlaceholderText("Enter your password");
        passwordInput->setEchoMode(QLineEdit::Password);

        QPushButton *loginButton = new QPushButton("Login", this);
        connect(loginButton, &QPushButton::clicked, this, &LoginWindow::onLoginClicked);

        // Create a layout for the form
        QVBoxLayout *formLayout = new QVBoxLayout;
        formLayout->addWidget(emailLabel);
        formLayout->addWidget(emailInput);
        formLayout->addWidget(passwordLabel);
        formLayout->addWidget(passwordInput);
        formLayout->addWidget(loginButton);
        formLayout->setSpacing(10);
        formLayout->setContentsMargins(20, 20, 20, 20); // Margins inside the form

        // Create a container widget for the form layout
        QWidget *formContainer = new QWidget(this);
        formContainer->setLayout(formLayout);
        formContainer->setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;");

        // Create a main layout and add the form container
        QVBoxLayout *mainLayout = new QVBoxLayout;
        mainLayout->addWidget(formContainer);
        mainLayout->setAlignment(Qt::AlignCenter); // Center the form container
        setLayout(mainLayout);

        // Set the fixed size of the form container
        formContainer->setFixedSize(300, 200);

        // Set fullscreen and center the window
        QScreen *screen = QApplication::primaryScreen();
        QRect screenGeometry = screen->availableGeometry();
        setGeometry(screenGeometry);

        showFullScreen();

        // Ensure the window remains on top and visible
        QTimer::singleShot(0, this, &LoginWindow::ensureWindowOnTop);
    }

private slots:
    void onLoginClicked() {
        QString email = emailInput->text();
        QString password = passwordInput->text();
        // Print the credentials (for debugging purposes)
        qDebug() << "Email:" << email;
        qDebug() << "Password:" << password;
        // You might want to add more logic to handle the login action
    }

    void ensureWindowOnTop() {
        // Reapply the always-on-top property
        setWindowFlags(windowFlags() | Qt::WindowStaysOnTopHint);
        show(); // Ensure the window is visible
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
