from PyQt6.QtWidgets import QMessageBox


def ShowPopup(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Information)

    # Add standard buttons and connect a handler
    msg.setStandardButtons(
        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
    )

    # Show the message box and wait for user interaction
    msg.exec()
