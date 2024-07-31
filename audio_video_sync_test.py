import device_connection
import white_box_rec
import beep_rec

find_cts_package = "shell pm list packages | findstr 'verifier'"
cts_package = "package:com.android.cts.verifier"
cts_activity = "shell am start -n com.android.cts.verifier/.projection.video.ProjectionVideoActivity"

is_verifier_installed = device_connection.execute_adb_command(find_cts_package)
if is_verifier_installed == cts_package:
    device_connection.launch_app(package_name = cts_package, activity_name = cts_activity)
# TODO install cts verifier apk and replace if-else for try-except-finally
