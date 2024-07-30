#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QScreen>
#include <QDebug>
#include <QTimer>
#include <QProcess>

class LoginWindow : public QWidget {
    Q_OBJECT

public:
    LoginWindow(QWidget *parent = nullptr) : QWidget(parent), process(new QProcess(this)) {
        setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);

        setStyleSheet("background-color: white;");

        QLabel *emailLabel = new QLabel("Email:", this);
        emailInput = new QLineEdit(this);
        emailInput->setPlaceholderText("Introdu-ti mail-ul");

        QLabel *passwordLabel = new QLabel("Parola:", this);
        passwordInput = new QLineEdit(this);
        passwordInput->setPlaceholderText("Introdu parola");
        passwordInput->setEchoMode(QLineEdit::Password);

        QPushButton *loginButton = new QPushButton("Intră în cont", this);
        connect(loginButton, &QPushButton::clicked, this, &LoginWindow::onLoginClicked);

        loginButton->setStyleSheet(
            "QPushButton {"
            "    background-color: #e0e0e0;"
            "    border: 1px solid #ccc;"
            "    padding: 10px;"
            "    font-size: 16px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #d0d0d0;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #c0c0c0;"
            "}");

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

        QStringList arguments;
        arguments << "start.py" << email << password;

        process->start("python3", arguments);

        connect(process, &QProcess::readyReadStandardOutput, [this]() {
            qDebug() << "Output:" << process->readAllStandardOutput();
        });

        connect(process, &QProcess::readyReadStandardError, [this]() {
            qDebug() << "Error:" << process->readAllStandardError();
        });

        connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), [this](int exitCode, QProcess::ExitStatus exitStatus) {
            if (exitStatus == QProcess::CrashExit) {
                qDebug() << "Process crashed with exit code:" << exitCode;
            } else {
                qDebug() << "Process finished with exit code:" << exitCode;
            }
            qDebug() << "Exiting application...";
            QApplication::quit();
        });

        if (!process->waitForStarted()) {
            qDebug() << "Failed to start process:" << process->errorString();
            QApplication::quit(); 
        } else {
            qDebug() << "Process started successfully.";
        }
    }

    void ensureWindowOnTop() {
        setWindowFlags(windowFlags() | Qt::WindowStaysOnTopHint);
        show();
    }

private:
    QLineEdit *emailInput;
    QLineEdit *passwordInput;
    QProcess *process;  
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    app.setStyleSheet("QPushButton {"
                      "    background-color: #e0e0e0;"
                      "    border: 1px solid #ccc;"
                      "    padding: 10px;"
                      "    font-size: 16px;"
                      "}"
                      "QPushButton:hover {"
                      "    background-color: #d0d0d0;"
                      "}"
                      "QPushButton:pressed {"
                      "    background-color: #c0c0c0;"
                      "}");

    LoginWindow loginWindow;
    loginWindow.show();

    return app.exec();
}

#include "main.moc"
