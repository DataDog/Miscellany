# This is used for testing in the vagrant box -- not for use with the custom check
import tempfile
import subprocess
stdout_f=tempfile.TemporaryFile()
stderr_f=tempfile.TemporaryFile()
# This will produce an error
#proc = subprocess.Popen(["free", "|", "grep", "Mem", "|", "awk", "'{print $3/$2 * 100.0}'"], stdout=stdout_f)
# can't get output
#proc = subprocess.Popen(["free | grep Mem | awk '{print $3/$2 * 100.0}'"], stdout=stdout_f, stderr=stderr_f, shell=True)
# can't get output
#proc = subprocess.Popen(["rand"], stdout=stdout_f, stderr=stderr_f, shell=True)
proc = subprocess.Popen(["rand"], stdout=stdout_f, stderr=stderr_f)
stdout_f.seek(0)
output = stdout_f.read()
print(output)
