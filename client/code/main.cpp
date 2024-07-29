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

class CompetitionCodeWindow : public QWidget {
    Q_OBJECT

public:
    CompetitionCodeWindow(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);

        setStyleSheet("background-color: white;");

        QLabel *codeLabel = new QLabel("Introduceți codul competiției:", this);
        codeInput = new QLineEdit(this);
        codeInput->setPlaceholderText("Enter competition code");

        submitButton = new QPushButton("Submit", this);
        connect(submitButton, &QPushButton::clicked, this, &CompetitionCodeWindow::onSubmitClicked);

        QVBoxLayout *formLayout = new QVBoxLayout;
        formLayout->addWidget(codeLabel);
        formLayout->addWidget(codeInput);
        formLayout->addWidget(submitButton);
        formLayout->setSpacing(10);
        formLayout->setContentsMargins(20, 20, 20, 20);

        QWidget *formContainer = new QWidget(this);
        formContainer->setLayout(formLayout);
        formContainer->setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;");

        QVBoxLayout *mainLayout = new QVBoxLayout;
        mainLayout->addWidget(formContainer);
        mainLayout->setAlignment(Qt::AlignCenter);
        setLayout(mainLayout);

        formContainer->setFixedSize(300, 150);

        QScreen *screen = QApplication::primaryScreen();
        QRect screenGeometry = screen->availableGeometry();
        setGeometry(screenGeometry);

        showFullScreen();

        QTimer::singleShot(0, this, &CompetitionCodeWindow::ensureWindowOnTop);
    }

private slots:
    void onSubmitClicked() {
        QString code = codeInput->text();
        qDebug() << "Competition Code:" << code;

        QProcess *process = new QProcess(this);

        connect(process, &QProcess::readyReadStandardOutput, [process]() {
            qDebug() << "Output:" << process->readAllStandardOutput();
        });

        connect(process, &QProcess::readyReadStandardError, [process]() {
            qDebug() << "Error:" << process->readAllStandardError();
        });

        connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), [process](int exitCode, QProcess::ExitStatus exitStatus) {
            if (exitStatus == QProcess::CrashExit) {
                qDebug() << "Process crashed with exit code:" << exitCode;
            } else {
                qDebug() << "Process finished with exit code:" << exitCode;
            }
        });

        QStringList arguments;
        arguments << "main.py" << code;
        process->start("python3", arguments);

        if (!process->waitForStarted()) {
            qDebug() << "Failed to start process:" << process->errorString();
        } else {
            qDebug() << "Process started successfully.";
        }

        QTimer::singleShot(500, qApp, &QApplication::quit); 
    }

    void ensureWindowOnTop() {
        setWindowFlags(windowFlags() | Qt::WindowStaysOnTopHint);
        show();
    }

private:
    QLineEdit *codeInput;
    QPushButton *submitButton;
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

    CompetitionCodeWindow competitionCodeWindow;
    competitionCodeWindow.show();

    return app.exec();
}

#include "main.moc"
