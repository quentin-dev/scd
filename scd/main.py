import PySimpleGUI as sg


from scd.logic.downloader import download_file


def run():
    sg.theme("DarkAmber")
    sg.user_settings_filename(filename="settings.json")
    layout = [
        [
            sg.Text("Save to"),
            sg.Input(
                f"{sg.user_settings_get_entry('-downloadroot-', './')}",
                key="-DOWNLOADROOTINPUT-",
            ),
            sg.FolderBrowse(),
            sg.Button("Set as default", key="-SETDOWNLOADROOT-"),
        ],
        [
            sg.Text("Comic URL"),
            sg.InputText(key="-URLINPUT-"),
            sg.Checkbox("Save in separate folder", key="-SEPARATEFOLDER-"),
            sg.Checkbox("Ignore year", key="-IGNOREYEAR-"),
        ],
        [sg.Button("Save"), sg.Button("Cancel"), sg.Text(key="-OUTPUTMESSAGE-")],
    ]

    window = sg.Window("sunbro's Comics Downloader", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "-SETDOWNLOADROOT-":
            sg.user_settings_set_entry("-downloadroot-", values["-DOWNLOADROOTINPUT-"])
        elif event == "Save":
            window.perform_long_operation(
                lambda: download_file(
                    url=values["-URLINPUT-"],
                    create_folder=values["-SEPARATEFOLDER-"],
                    ignore_year=values["-IGNOREYEAR-"],
                ),
                "-DOWNLOADED-",
            )
            window["-URLINPUT-"].update("")  # Clear URL
            window["-OUTPUTMESSAGE-"].update("Downloading ...")
        elif event == "-DOWNLOADED-":
            window["-OUTPUTMESSAGE-"].update("Download successful")

    window.close()


if __name__ == "__main__":
    run()
